from django.contrib import messages
from django.core import exceptions
from django.shortcuts import render
from django.views import View

from . import models as resource_models
from . import utils


class NotificationListView(View):
    template_name = "resources/notifications.html"

    def mark_all_read(self, user):
        notifications = utils.get_notifications_to_list(user=user)
        for notification in notifications:
            notification.mark_notification_as_read()

        return

    def mark_notification_read(self, request, notification_id):
        try:
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.mark_notification_as_read()
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "Notification not found")
        except exceptions.MultipleObjectsReturned:
            messages.error(request, "Oops, could not delete notification")
            print("Multiple notifications found with same notification id")

        return

    def mark_notification_unread(self, request, notification_id):
        try:
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.mark_notification_as_unread()
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "Notification not found")
        except exceptions.MultipleObjectsReturned:
            messages.error(request, "Oops, could not delete notification")
            print("Multiple notifications found with same notification id")

        return

    def restore_notification(self, request, notification_id):
        try:
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.restore_notification()
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "Notification not found")
        except exceptions.MultipleObjectsReturned:
            messages.error(request, "Oops, could not delete notification")
            print("Multiple notifications found with same notification id")

        return

    def delete_notification(self, request, notification_id):
        try:
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.delete_notification()
        except exceptions.ObjectDoesNotExist:
            messages.error(request, "Notification not found")
        except exceptions.MultipleObjectsReturned:
            messages.error(request, "Oops, could not delete notification")
            print("Multiple notifications found with same notification id")

        return

    def get(self, request):
        context = {
            "notification_list": [],
            "deleted_notifications": [],
        }

        notification_id = None

        if "markall" in request.GET:
            self.mark_all_read(user=request.user)
        elif "markread" in request.GET:
            notification_id = request.GET["markread"]
            self.mark_notification_read(
                request=request, notification_id=notification_id
            )
        elif "markunread" in request.GET:
            notification_id = request.GET["markunread"]
            self.mark_notification_unread(
                request=request, notification_id=notification_id
            )
        elif "restorenotification" in request.GET:
            notification_id = request.GET["restorenotification"]
            self.mark_notification_unread(
                request=request, notification_id=notification_id
            )

        notification_list = utils.get_notifications_to_list(user=request.user)
        deleted_notifications = utils.get_deleted_notifications(user=request.user)

        context["notification_list"] = notification_list
        context["deleted_notifications"] = deleted_notifications

        return render(request, self.template_name, context)

    def post(self, request):
        context = {
            "notification_list": [],
            "deleted_notifications": [],
        }

        if "delete" in request.POST:
            notification_id = request.POST["delete"]
            self.delete_notification(request=request, notification_id=notification_id)

        notification_list = utils.get_notifications_to_list(user=request.user)
        deleted_notifications = utils.get_deleted_notifications(user=request.user)

        context["notification_list"] = notification_list
        context["deleted_notifications"] = deleted_notifications

        return render(request, self.template_name, context)
