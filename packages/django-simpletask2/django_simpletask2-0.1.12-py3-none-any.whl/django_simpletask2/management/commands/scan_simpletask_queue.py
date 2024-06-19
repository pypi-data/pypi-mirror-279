from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps

from django_simpletask2.models import SimpleTaskQueue
from django_simpletask2.models import SimpleTask


class Command(BaseCommand):
    help = "Collect All SimpleTask Models."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        model_strings = set()
        queues = {}
        for queue in SimpleTaskQueue.objects.all():
            queues[queue.model] = queue

        for model in apps.get_models():
            if issubclass(model, SimpleTask):
                model_string = ".".join([model._meta.app_label, model._meta.model_name])
                model_strings.add(model_string)
                queue = queues.get(model_string, None)
                if not queue:
                    queue = SimpleTaskQueue()
                    queue.name = model._meta.verbose_name
                    queue.model = model_string
                    queue.alive = True
                    queue.alive_update_time = timezone.now()
                    queue.save()
                    print(
                        """New Queue "{verbose_name}"[{model_string}] discovered...""".format(
                            verbose_name=model._meta.verbose_name,
                            model_string=model_string,
                        )
                    )
                else:
                    if not queue.alive:
                        queue.alive = True
                        queue.alive_update_time = timezone.now()
                        queue.save()
                        print(
                            """Old Queue "{verbose_name}"[{model_string}] recovered...""".format(
                                verbose_name=model._meta.verbose_name,
                                model_string=model_string,
                            )
                        )
                    if queue.name != model._meta.verbose_name:
                        queue.name = model._meta.verbose_name
                        queue.save()
                        print(
                            """Old Queue "{verbose_name}"[{model_string}] name updated...""".format(
                                verbose_name=model._meta.verbose_name,
                                model_string=model_string,
                            )
                        )
            for model_string, queue in queues.items():
                if not model_string in model_strings:
                    queue.alive = False
                    queue.alive_update_time = timezone.now()
                    queue.save()
