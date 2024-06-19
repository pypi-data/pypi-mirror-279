import re
import uuid
import logging
from django.apps import apps
from django.utils import timezone
from django_redis import get_redis_connection
from .models import SimpleTaskChannel
from .models import SimpleTaskQueue
from .models import SimpleTask
from .settings import DJANGO_SIMPLETASK2_CHANNEL_NAME_TEMPLATE
from .settings import DJANGO_SIMPLETASK2_TASK_PULL_TIMEOUT
from .settings import DJANGO_SIMPLETASK2_CHANNEL_NAME_STRIP_REGEX
from .settings import DJANGO_SIMPLETASK2_CHANNEL_FLAGS_TEMPLATE
from .exceptions import DjangoSimpleTask2Error
from .viewshelper import get_task_instance

_logger = logging.getLogger(__name__)


def do_auto_reset():
    infos = {
        "auto_reset": {},
    }
    for ModelClass in apps.get_models():
        if issubclass(ModelClass, SimpleTask):
            model_class_name = "{app_label}.{model_name}".format(
                app_label=ModelClass._meta.app_label,
                model_name=ModelClass._meta.model_name,
            )
            number = ModelClass.do_auto_reset()
            infos["auto_reset"][model_class_name] = number
    infos["remove_duplicate_items"] = remove_duplicate_items_for_all_channels()
    infos["update_channel_queue_size"] = update_channel_queue_size_for_all_channels()
    return infos


def do_task(payload):
    task_info = payload.get("task_info", None)
    if not task_info:
        raise DjangoSimpleTask2Error(2910015, "`task_info` field is required.")

    try:
        task_instance = get_task_instance(task_info)
    except DjangoSimpleTask2Error as error:
        raise error
    except Exception as error:
        _logger.warning("get task instance %s failed with error: %s.", task_info, error)
        message = "get task instance {task_info} failed with error: {error}.".format(
            task_info=task_info, error=str(error)
        )
        raise DjangoSimpleTask2Error(2910016, message)

    try:
        result = task_instance.do_task(payload)
        return result
    except DjangoSimpleTask2Error as error:
        _logger.info("do task got failed: {error}".format(error=str(error)))
        raise error
    except Exception as error:
        _logger.error("system error: {error}".format(error=str(error)))
        raise error


def get_a_task(channels="default"):
    redis_conn = SimpleTask.get_redis_conn()
    channels = [
        DJANGO_SIMPLETASK2_CHANNEL_NAME_TEMPLATE.format(channel=channel)
        for channel in channels.split(",")
    ]
    task = redis_conn.blpop(channels, timeout=DJANGO_SIMPLETASK2_TASK_PULL_TIMEOUT)
    if not task:
        _logger.debug(
            "got NO task whiling pulling task from channels: {channels}".format(
                channels=channels
            )
        )
        return None
    else:
        _logger.debug("got task {task}.".format(task=task))
    channel_fullname, task_info = task
    try:
        channel = re.match(
            DJANGO_SIMPLETASK2_CHANNEL_NAME_STRIP_REGEX, channel_fullname
        ).groupdict()["channel"]
        channel_flags = DJANGO_SIMPLETASK2_CHANNEL_FLAGS_TEMPLATE.format(
            channel=channel
        )
        result = redis_conn.srem(channel_flags, task_info)
        if result != 1:
            _logger.warning(
                "clean task flag failed: channel_flags={channel_flags}, task_info={task_info}.".format(
                    channel_flags=channel_flags, task_info=task_info
                )
            )
    except Exception as error:
        _logger.warning(
            "clean task flag got unknown exception: channel_flags={channel_flags}, task_info={task_info}, error={error}".format(
                channel_flags=channel_flags,
                task_info=task_info,
                error=str(error),
            )
        )
    return task_info


def update_queue_size():
    info = {}
    for queue in SimpleTaskQueue.objects.filter(alive=True).all():
        if queue.enabled is not False:
            queue_model = apps.get_model(queue.model)
            queue_size = queue_model.objects.count()
            ready_size = queue_model.objects.filter(status=queue_model.READY).count()
            doing_size = queue_model.objects.filter(status=queue_model.DOING).count()
            done_size = queue_model.objects.filter(status=queue_model.DONE).count()
            success_size = queue_model.objects.filter(success=True).count()
            fail_size = queue_model.objects.filter(success=False).count()
            unknown_size = queue_model.objects.filter(success=None).count()
            if queue.size != queue_size:
                queue.size = queue_size
            if queue.ready_size != ready_size:
                queue.ready_size = ready_size
            if queue.doing_size != doing_size:
                queue.doing_size = doing_size
            if queue.done_size != done_size:
                queue.done_size = done_size
            if queue.success_size != success_size:
                queue.success_size = success_size
            if queue.fail_size != fail_size:
                queue.fail_size = fail_size
            if queue.unknown_size != unknown_size:
                queue.unknown_size = unknown_size
            queue.size_update_time = timezone.now()
            queue.save()
            info[queue.model] = {
                "size": queue.size,
                "ready_size": queue.ready_size,
                "doing_size": queue.doing_size,
                "done_size": queue.done_size,
                "success_size": queue.success_size,
                "fail_size": queue.fail_size,
                "unknown_size": queue.unknown_size,
                "update_time": timezone.make_naive(queue.size_update_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
    return info


def update_channel_size(ids=None):
    info = {}
    if ids:
        ids = [int(x) for x in ids]
        queryset = SimpleTaskChannel.objects.filter(pk__in=ids)
    else:
        queryset = SimpleTaskChannel.objects
    for channel in queryset.all():
        redis_key = channel.get_channel_redis_key()
        redis_name = channel.get_channel_redis_name()
        db = get_redis_connection(redis_name)
        size = db.llen(redis_key)
        if channel.queue_size != size:
            channel.queue_size = size
        channel.queue_size_update_time = timezone.now()
        channel.save()
        info[redis_key] = size
    return info


def clean_all_items(channel_id):
    # 删除指定消息队列
    channel = SimpleTaskChannel.objects.get(pk=channel_id)
    redis_key = channel.get_channel_redis_key()
    redis_name = channel.get_channel_redis_name()
    db = get_redis_connection(redis_name)
    result = db.delete(redis_key)
    # 完成后，更新一下统计数据
    update_channel_size(ids=[channel_id])
    return result


def get_channel(channel):
    if isinstance(channel, SimpleTaskChannel):
        return channel
    if isinstance(channel, str):
        return SimpleTaskChannel.objects.get(code=channel)
    if isinstance(channel, int):
        return SimpleTaskChannel.objects.get(pk=channel)
    raise SimpleTaskChannel.DoesNotExist()


def remove_duplicate_items(channel):
    """清理指定队列的重复项。"""
    channel = get_channel(channel)
    redis_key = channel.get_channel_redis_key()
    redis_name = channel.get_channel_redis_name()
    db = get_redis_connection(redis_name)
    # 队列为空时，后续操作为产生no such key的错误。
    # 这里提前判断是否为空队列，提前结束处理过程。
    if not db.exists(redis_key):
        return {
            "before": 0,
            "after": 0,
        }
    # 去重操作
    swap_redis_key_suffix = str(uuid.uuid4())
    swap_redis_key = "__".join(["swap", redis_key, swap_redis_key_suffix])
    db.rename(redis_key, swap_redis_key)
    items = db.lrange(swap_redis_key, 0, -1)
    unique_items = list(set(items))
    if unique_items:
        db.lpush(redis_key, *unique_items)
    db.delete(swap_redis_key)
    # 完成后，更新一下统计数据
    update_channel_size(ids=[channel_id])
    return {
        "before": len(items),
        "after": len(unique_items),
    }


def remove_duplicate_items_for_all_channels():
    """清理所有队列的重复项。"""
    result = {}
    for channel in SimpleTaskChannel.objects.all():
        result[channel.code] = remove_duplicate_items(channel)
    return result


def update_channel_queue_size(channel):
    """更新指定队列长度统计数。"""
    channel = get_channel(channel)
    redis_key = channel.get_channel_redis_key()
    redis_name = channel.get_channel_redis_name()
    db = get_redis_connection(redis_name)
    if not db.exists(redis_key):
        queue_size = 0
    else:
        queue_size = db.llen(redis_key)
    channel.queue_size = queue_size
    channel.queue_size_update_time = timezone.now()
    channel.save()
    return channel.queue_size


def update_channel_queue_size_for_all_channels():
    """更新所有队列长度统计数。"""
    result = {}
    for channel in SimpleTaskChannel.objects.all():
        result[channel.code] = update_channel_queue_size(channel)
    return result
