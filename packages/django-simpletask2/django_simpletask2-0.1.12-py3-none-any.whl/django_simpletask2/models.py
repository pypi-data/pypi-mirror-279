import logging
import datetime

from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_redis import get_redis_connection
from globallock import GlobalLockManager

from .exceptions import DjangoSimpleTask2Error
from .settings import DJANGO_SIMELETASK2_GLOBAL_LOCK_CONFIG
from .settings import DJANGO_SIMPLETASK2_TASK_LOCK_NAME_TEMPLATE
from .settings import DJANGO_SIMPLETASK2_REDIS_NAME
from .settings import DJANGO_SIMPLETASK2_TASK_WAIT_TIMEOUT_KEY_TEMPLATE
from .settings import DJANGO_SIMPLETASK2_DO_TASK_TIMEOUT_KEY_TEMPLATE
from .settings import DJANGO_SIMPLETASK2_CHANNEL_NAME_TEMPLATE
from .settings import DJANGO_SIMPLETASK2_CHANNEL_FLAGS_TEMPLATE

logger = logging.getLogger(__name__)


class SimpleTask(models.Model):
    READY = 10
    DOING = 20
    DONE = 30
    STATUS = [
        (READY, _("Ready")),
        (DOING, _("Doing")),
        (DONE, _("Done")),
    ]

    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    mod_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))
    status = models.IntegerField(
        choices=STATUS, default=READY, verbose_name=_("Status"), editable=False
    )
    start_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Start Time"), editable=False
    )
    current_step = models.IntegerField(
        null=True, blank=True, verbose_name=_("Current Step"), editable=False
    )
    step1_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Step1 start time"), editable=False
    )
    step2_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Step2 start time"), editable=False
    )
    step3_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Step3 start time"), editable=False
    )
    done_time = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Done Time"), editable=False
    )
    success = models.BooleanField(
        null=True, verbose_name=_("Success Status"), editable=False
    )
    auto_reset_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Auto Reset Time"),
        help_text=_("After which time the task should be reset."),
        editable=False,
    )

    is_multi_steps = False
    final_step = 1
    do_task_timeout = 300
    task_wait_timeout = 300
    SIMPLE_TASK_FIELDS = [
        "status",
        "success",
        "current_step_display",
        "add_time",
        "start_time",
        "auto_reset_time",
        "done_time",
        "mod_time",
        "step1_time",
        "step2_time",
        "step3_time",
    ]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            created = True
            self.auto_reset_time = timezone.now() + datetime.timedelta(
                seconds=self.get_task_wait_timeout()
            )
        else:
            created = False
        super().save(*args, **kwargs)
        if created:
            # 新建的情况下
            # 需要向消息队列推送任务
            # 但需要在完成commit后推送
            transaction.on_commit(lambda: self.push_to_mq())

    @classmethod
    def get_redis_conn(cls):
        return get_redis_connection(DJANGO_SIMPLETASK2_REDIS_NAME)

    def get_task_wait_timeout(self):
        redis_conn = self.get_redis_conn()
        task_wait_timeout_key = (
            DJANGO_SIMPLETASK2_TASK_WAIT_TIMEOUT_KEY_TEMPLATE.format(
                channel=self.get_channel_name()
            )
        )
        timeout = redis_conn.get(task_wait_timeout_key)
        if timeout:
            timeout = int(timeout)
        return timeout or self.task_wait_timeout

    def get_do_task_timeout(self):
        redis_conn = self.get_redis_conn()
        task_wait_timeout_key = DJANGO_SIMPLETASK2_DO_TASK_TIMEOUT_KEY_TEMPLATE.format(
            channel=self.get_channel_name()
        )
        timeout = redis_conn.get(task_wait_timeout_key)
        if timeout:
            timeout = int(timeout)
        return timeout or self.do_task_timeout

    def get_task_info(self):
        return "{app_label}.{model_name}:{task_id}".format(
            app_label=self._meta.app_label,
            model_name=self._meta.model_name,
            task_id=self.pk,
        )

    def get_channel_name(self):
        if hasattr(self, "channel_field"):
            channel_field = getattr(self, "channel_field")
            return getattr(self, channel_field, "default")
        else:
            return "default"

    get_channel_name.short_description = _("Channel")

    def get_task_queue_name(self):
        channel_name = self.get_channel_name()
        return DJANGO_SIMPLETASK2_CHANNEL_NAME_TEMPLATE.format(channel=channel_name)

    def get_task_flags_name(self):
        channel_name = self.get_channel_name()
        return DJANGO_SIMPLETASK2_CHANNEL_FLAGS_TEMPLATE.format(channel=channel_name)

    def final_step_number(self):
        return self.final_step

    final_step_number.short_description = _("Final Step Number")

    def current_step_display(self):
        return "{current_step}/{final_step}".format(
            current_step=self.current_step or 0, final_step=self.final_step
        )

    current_step_display.short_description = _("Current Step")

    @classmethod
    def do_auto_reset(cls):
        now = timezone.now()
        counter = 0
        for item in (
            cls.objects.exclude(auto_reset_time=None)
            .exclude(status=cls.DONE)
            .filter(auto_reset_time__lt=now)
            .all()
        ):
            item.reset()
            transaction.on_commit(lambda: item.push_to_mq())
            counter += 1
        for item in cls.objects.filter(status=cls.READY, auto_reset_time=None).all():
            item.reset()
            transaction.on_commit(lambda: item.push_to_mq())
            counter += 1
        return counter

    def reset(self, save=True):
        self.status = self.READY
        self.start_time = None
        self.current_step = None
        self.done_time = None
        self.step1_time = None
        self.step2_time = None
        self.step3_time = None
        self.success = None
        self.auto_reset_time = timezone.now() + datetime.timedelta(
            seconds=self.get_task_wait_timeout()
        )
        if save:
            self.save()
        return self

    def push_to_mq(self):
        channel_name = self.get_channel_name()
        task_queue_name = self.get_task_queue_name()
        task_flags_name = self.get_task_flags_name()
        task_info = "{app_label}.{model_name}:{task_id}".format(
            app_label=self._meta.app_label,
            model_name=self._meta.model_name,
            task_id=self.pk,
        )
        redis_conn = self.get_redis_conn()
        redis_conn.sadd(task_flags_name, task_info)
        redis_conn.rpush(task_queue_name, task_info)
        return self

    def start(self, force=False, save=True):
        if force or self.status == self.READY:
            self.status = self.DOING
            self.start_time = timezone.now()
            self.auto_reset_time = self.start_time + datetime.timedelta(
                seconds=self.get_do_task_timeout()
            )
            if save:
                self.save()
            return True
        return False

    def done(self, force=False, save=True):
        if force or self.status == self.DOING:
            self.status = self.DONE
            self.done_time = timezone.now()
            self.auto_reset_time = None
            if save:
                self.save()
            return True
        return False

    def do_task(self, payload=None, force=False):
        app_label = self._meta.app_label
        model_name = self._meta.model_name
        lockman = GlobalLockManager(DJANGO_SIMELETASK2_GLOBAL_LOCK_CONFIG)
        lockname = DJANGO_SIMPLETASK2_TASK_LOCK_NAME_TEMPLATE.format(
            app_label=app_label,
            model_name=model_name,
            task_id=self.pk,
        )
        timeout = self.get_do_task_timeout()
        with lockman.lock(lockname, timeout=timeout) as lock:
            if lock.is_locked:
                task = self.__class__.objects.get(pk=self.pk)
                if not force and task.status == self.DONE:
                    message = "task {task_info} already done, to do NOTHING.".format(
                        task_info=self.get_task_info()
                    )
                    raise DjangoSimpleTask2Error(2910015, message)
                return self._do_task(payload, force)
            else:
                message = "task {task_info} locked by another worker.".format(
                    task_info=self.get_task_info()
                )
                raise DjangoSimpleTask2Error(2910013, message)

    def _do_task(self, payload=None, force=False):
        payload = payload or {}
        step = payload.get("step", 1)
        handler_name = "do_task_main_step{step}".format(step=step)
        handler = getattr(self, handler_name, None)
        if not handler:
            message = "task handler is not implemented, task={app_label}.{model_name}, handler={handler_name}.".format(
                app_label=self._meta.app_label,
                model_name=self._meta.model_name,
                handler_name=handler_name,
            )
            raise DjangoSimpleTask2Error(2910007, message)

        setattr(self, "step{}_time".format(step), timezone.now())
        self.current_step = step
        if step == 1:
            if not self.start(force=force):
                message = "task {task_info} status is not READY but {status}, you can NOT start it.".format(
                    task_info=self.get_task_info(),
                    status=self.get_status_display(),
                )
                logger.error(message)
                raise DjangoSimpleTask2Error(2910008, message)

        continue_flag = True
        if self.final_step == step:
            continue_flag = False

        try:
            data = handler(payload)
        except Exception as error:
            message = "task {task_info} calling {handler_name} failed with error message: {error}.".format(
                task_info=self.get_task_info(),
                handler_name=handler_name,
                error=str(error),
            )
            try:
                self.status = self.DONE
                self.done_time = timezone.now()
                self.auto_reset_time = None
                self.success = False
                self.save()
            except Exception as error:
                message = message[
                    :-1
                ] + ", and also failed to save status with error: {error}.".format(
                    error=str(error)
                )
            logger.error(message)
            raise DjangoSimpleTask2Error(2910009, message)
        try:
            if self.final_step == step:
                self.status = self.DONE
                self.done_time = timezone.now()
                self.auto_reset_time = None
                self.success = True
            self.save()
            return {
                "continue_flag": continue_flag,
                "task_info": self.get_task_info(),
                "next_step": step + 1,
                "data": data,
            }
        except Exception as error:
            message = "task {task_info}} failed to save status with error message: {error}.".format(
                task_info=self.get_task_info(),
                error=str(error),
            )
            logger.error(message)
            raise DjangoSimpleTask2Error(2910014, message)

    def do_task_main(self, payload=None):
        raise NotImplementedError(
            "{class_name}.do_task_main NOT implemented error.".format(
                class_name=self.__class__.__name__
            )
        )

    def do_task_main_step1(self, payload=None):
        return self.do_task_main(payload)


class SimpleTaskChannel(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("Channel Code"),
    )
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("Channel Name"),
    )
    redis_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("Channel Cache Name"),
    )
    redis_key = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("Channel Key"),
    )
    queue_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Channel Queue Size"),
    )
    queue_size_update_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Channel Queue Size Update Time"),
    )
    add_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Add Time"),
    )
    mod_time = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Modify Time"),
    )

    class Meta:
        verbose_name = _("Django Simple Task Channel")
        verbose_name_plural = _("Django Simple Task Channels")
        permissions = [
            (
                "simpletaskchannel_clean_all_items",
                _("Can clean all items"),
            ),
            (
                "simpletaskchannel_remove_duplicate_items",
                _("Can remove duplicate items"),
            ),
            (
                "simpletaskchannel_update_channel_queue_size",
                _("Can update channel queue size"),
            ),
        ]

    def __str__(self):
        return self.name or self.code

    def get_channel_redis_name(self):
        return self.redis_name or DJANGO_SIMPLETASK2_REDIS_NAME

    def get_channel_redis_key(self):
        return DJANGO_SIMPLETASK2_CHANNEL_NAME_TEMPLATE.format(
            channel=self.code,
        )

    def get_channel_queue_size(self):
        db = get_redis_connection(self.get_channel_redis_name())
        return db.llen(self.get_channel_redis_key())

    def update_queue_size(self, save=True):
        self.queue_size = self.get_channel_queue_size()
        self.queue_size_update_time = timezone.now()
        if save:
            self.save()
        return self


class SimpleTaskQueue(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name=_("Simple Task Queue Name"),
    )
    model = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Model"),
    )
    alive = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Alive"),
        help_text=_("Simple Task Queue alive means the model is NOT deleted."),
    )
    alive_update_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Alive Status Update Time"),
    )
    enabled = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Enabled"),
        help_text=_("Will not update the queue stats if the queue is disabled."),
    )
    size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Size"),
        help_text=_(
            "The queue size is calculated periodically, so it may delay some times. Check the details to find the lastest update time."
        ),
    )
    ready_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Ready Size"),
    )
    doing_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Doing Size"),
    )
    done_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Done Size"),
    )
    success_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Success Size"),
    )
    fail_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Fail Size"),
    )
    unknown_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Unknown Size"),
    )
    size_update_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Simple Task Queue Size Update Time"),
    )
    add_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Add Time"),
    )
    mod_time = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Modify Time"),
    )

    class Meta:
        verbose_name = _("Simple Task Queue")
        verbose_name_plural = _("Simple Task Queues")

    def __str__(self):
        return self.name
