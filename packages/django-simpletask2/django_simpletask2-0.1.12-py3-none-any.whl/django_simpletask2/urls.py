from django.urls import path
from . import views

urlpatterns = [
    path(
        "do_task",
        views.do_task,
        name="django_simpletask2.do_task",
    ),
    path(
        "get_a_task",
        views.get_a_task,
        name="django_simpletask2.get_a_task",
    ),
    path(
        "do_auto_reset",
        views.do_auto_reset,
        name="django_simpletask2.do_auto_reset",
    ),
    path(
        "update_queue_size",
        views.update_queue_size,
        name="django_simpletask2.update_queue_size",
    ),
    path(
        "update_channel_size",
        views.update_channel_size,
        name="django_simpletask2.update_channel_size",
    ),
]
