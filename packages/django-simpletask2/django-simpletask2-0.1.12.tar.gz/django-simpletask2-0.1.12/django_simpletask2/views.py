import re
import logging

from django.views.decorators.csrf import csrf_exempt

from .viewshelper import json_apiview
from .viewshelper import aclkey_check
from .viewshelper import get_payload
from .settings import *
from . import services

logger = logging.getLogger(__name__)


@csrf_exempt
@json_apiview
def do_auto_reset(request):
    payload = get_payload(request)
    aclkey_check(payload)
    return services.do_auto_reset()


@csrf_exempt
@json_apiview
def do_task(request):
    payload = get_payload(request)
    aclkey_check(payload)
    return services.do_task(payload)


@csrf_exempt
@json_apiview
def get_a_task(request):
    payload = get_payload(request)
    aclkey_check(payload)
    channels = payload.get("channels", "default")
    return services.get_a_task(channels)


@csrf_exempt
@json_apiview
def update_queue_size(request):
    aclkey_check(request.GET)
    return services.update_queue_size()


@csrf_exempt
@json_apiview
def update_channel_size(request):
    aclkey_check(request.GET)
    return services.update_channel_size()


@csrf_exempt
@json_apiview
def clean_all_items(request):
    aclkey_check(request.GET)
    channel_id = int(request.GET.get("channel_id"))
    return services.clean_all_items(channel_id)


@csrf_exempt
@json_apiview
def remove_duplicate_items(request):
    aclkey_check(request.GET)
    channel_id = int(request.GET.get("channel_id"))
    return services.remove_duplicate_items(channel_id)
