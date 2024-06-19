from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.urls import path
from django.http import JsonResponse
from django_middleware_global_request import get_request

from .models import SimpleTaskQueue
from .models import SimpleTaskChannel
from .settings import DJANGO_SIMPLETASK2_GOTO_THE_QUEUE_CHANGELIST_TARGET
from . import services


class SimpleTaskQueueAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "enabled_display",
        "size",
        "ready_size",
        "doing_size",
        "done_size",
        "success_size",
        "fail_size",
        "unknown_size",
        "link_to_the_queue_changelist",
    ]
    list_filter = [
        "alive",
        "enabled",
    ]
    search_fields = [
        "name",
        "model",
    ]

    def enabled_display(self, obj):
        if obj.enabled is None:
            return obj.alive
        else:
            return obj.enabled

    enabled_display.short_description = _("Simple Task Queue Enabled")
    enabled_display.boolean = True

    def link_to_the_queue_changelist(self, obj):
        app_label, model_name = obj.model.split(".")
        url = reverse(
            "admin:{app_label}_{model_name}_changelist".format(
                app_label=app_label,
                model_name=model_name,
            )
        )
        target = DJANGO_SIMPLETASK2_GOTO_THE_QUEUE_CHANGELIST_TARGET or ""
        label = _("Goto The Queue List")
        return mark_safe(
            """<a href="{url}" target="{target}">{label}</a>""".format(
                url=url,
                target=target,
                label=label,
            )
        )

    link_to_the_queue_changelist.short_description = _("Operations")


class SimpleTaskChannelAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "name",
        "queue_size",
        "operations",
    ]
    search_fields = [
        "code",
        "name",
    ]

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path(
                "<path:object_id>/clean_all_items/",
                self.admin_site.admin_view(self.clean_all_items),
                name="%s_%s_clean_all_itemse" % info,
            ),
            path(
                "<path:object_id>/remove_duplicate_items/",
                self.admin_site.admin_view(self.remove_duplicate_items),
                name="%s_%s_remove_duplicate_items" % info,
            ),
            path(
                "<path:object_id>/update_channel_queue_size/",
                self.admin_site.admin_view(self.update_channel_queue_size),
                name="%s_%s_update_channel_queue_size" % info,
            ),
        ] + super().get_urls()

    def clean_all_items(self, request, object_id):
        info = self.model._meta.app_label, self.model._meta.model_name
        permtag = "%s:%s_clean_all_items" % info
        if not request.user.has_perm(permtag):
            return JsonResponse(
                {
                    "code": 1,
                    "message": "Access Deined!",
                    "result": None,
                }
            )
        code = 0
        message = "OK"
        result = None
        try:
            object_id = int(object_id)
            result = services.clean_all_items(object_id)
        except Exception as error:
            code = 2
            message = _("Clean all items failed: error={}").format(error)
        return JsonResponse(
            {
                "code": code,
                "message": message,
                "result": result,
            }
        )

    def remove_duplicate_items(self, request, object_id):
        info = self.model._meta.app_label, self.model._meta.model_name
        permtag = "%s:%s_remove_duplicate_items" % info
        if not request.user.has_perm(permtag):
            return JsonResponse(
                {
                    "code": 1,
                    "message": "Access Deined!",
                    "result": None,
                }
            )
        code = 0
        message = "OK"
        result = None
        try:
            object_id = int(object_id)
            result = services.remove_duplicate_items(object_id)
        except Exception as error:
            code = 2
            message = _("Remove duplicate items failed: error={}").format(error)
        return JsonResponse(
            {
                "code": code,
                "message": message,
                "result": result,
            }
        )

    def update_channel_queue_size(self, request, object_id):
        info = self.model._meta.app_label, self.model._meta.model_name
        permtag = "%s:%s_update_channel_queue_size" % info
        if not request.user.has_perm(permtag):
            return JsonResponse(
                {
                    "code": 1,
                    "message": "Access Deined!",
                    "result": None,
                }
            )
        code = 0
        message = "OK"
        result = None
        try:
            object_id = int(object_id)
            queue_size = services.update_channel_queue_size(object_id)
        except Exception as error:
            code = 2
            message = _("Update channel's queue size: error={}").format(error)
        return JsonResponse(
            {
                "code": code,
                "message": message,
                "result": queue_size,
            }
        )

    def operations(self, obj):
        info = self.model._meta.app_label, self.model._meta.model_name
        request = get_request()
        action_request_failed_message = _("Action request failed...")

        clean_all_items_permtag = "%s:%s_clean_all_items" % info
        clean_all_items_label = _("Clean All Items")
        clean_all_items_confirm_message = _("Are you sure to clean all items?")
        clean_all_items_request_url = reverse(
            "admin:%s_%s_clean_all_itemse" % info,
            kwargs={
                "object_id": obj.pk,
            },
        )
        clean_all_items_button = """
        <a href="{clean_all_items_request_url}" 
                class="django_simpletask2_channel_admin_button django_simpletask2_channel_admin_clean_all_items"
                confirm-message="{clean_all_items_confirm_message}"
                action-request-failed-message="{action_request_failed_message}"
                >
            <i class="fas fa-remove"></i> {clean_all_items_label}
        </a>""".format(
            clean_all_items_label=clean_all_items_label,
            clean_all_items_confirm_message=clean_all_items_confirm_message,
            clean_all_items_request_url=clean_all_items_request_url,
            action_request_failed_message=action_request_failed_message,
        )

        remove_duplicate_items_permtag = "%s:%s_remove_duplicate_items" % info
        remove_duplicate_items_label = _("Remove Duplicate Items")
        remove_duplicate_items_confirm_message = _(
            "Are you sure to remove duplicate items?"
        )
        remove_duplicate_items_request_url = reverse(
            "admin:%s_%s_remove_duplicate_items" % info,
            kwargs={
                "object_id": obj.pk,
            },
        )
        remove_duplicate_items_button = """
        <a href="{remove_duplicate_items_request_url}"
                class="django_simpletask2_channel_admin_button django_simpletask2_channel_admin_remove_duplicate_items"
                confirm-message="{remove_duplicate_items_confirm_message}"
                action-request-failed-message="{action_request_failed_message}"
                >
            <i class="fas fa-recycle"></i> {remove_duplicate_items_label}
        </a>
        """.format(
            remove_duplicate_items_label=remove_duplicate_items_label,
            remove_duplicate_items_confirm_message=remove_duplicate_items_confirm_message,
            remove_duplicate_items_request_url=remove_duplicate_items_request_url,
            action_request_failed_message=action_request_failed_message,
        )

        update_channel_queue_size_permtag = "%s:%s_update_channel_queue_size" % info
        update_channel_queue_size_label = _("Update Channel's Queue Size")
        update_channel_queue_size_confirm_message = _(
            "Are you sure to update the channel's queue size?"
        )
        update_channel_queue_size_request_url = reverse(
            "admin:%s_%s_update_channel_queue_size" % info,
            kwargs={
                "object_id": obj.pk,
            },
        )
        update_channel_queue_size_button = """
        <a href="{update_channel_queue_size_request_url}"
                class="django_simpletask2_channel_admin_button django_simpletask2_channel_admin_update_channel_queue_size"
                confirm-message="{update_channel_queue_size_confirm_message}"
                action-request-failed-message="{action_request_failed_message}"
                >
            <i class="fas fa-sync"></i> {update_channel_queue_size_label}
        </a>
        """.format(
            update_channel_queue_size_label=update_channel_queue_size_label,
            update_channel_queue_size_confirm_message=update_channel_queue_size_confirm_message,
            update_channel_queue_size_request_url=update_channel_queue_size_request_url,
            action_request_failed_message=action_request_failed_message,
        )

        buttons = []
        if request.user.has_perm(clean_all_items_permtag):
            buttons.append(clean_all_items_button)
        if request.user.has_perm(remove_duplicate_items_permtag):
            buttons.append(remove_duplicate_items_button)
        if request.user.has_perm(update_channel_queue_size_permtag):
            buttons.append(update_channel_queue_size_button)

        return mark_safe(" | ".join(buttons))

    operations.short_description = _("Operations")

    class Media:
        css = {
            "all": [
                "fontawesome/css/all.min.css",
                "jquery-ui/jquery-ui.min.css",
                "jquery-ui/themes/ui-lightness/theme.css",
                "django_simpletask2/css/django_simpletask2.css",
            ]
        }
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "jquery-ui/jquery-ui.min.js",
            "jquery-ui/i18n/datepicker-zh-Hans.js",
            "django_simpletask2/js/django_simpletask2.js",
            "admin/js/jquery.init.js",
        ]


admin.site.register(SimpleTaskQueue, SimpleTaskQueueAdmin)
admin.site.register(SimpleTaskChannel, SimpleTaskChannelAdmin)
