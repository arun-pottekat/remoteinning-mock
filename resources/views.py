from django.core import exceptions
from django.http import HttpResponseNotFound
from django.shortcuts import render

from . import models as resource_models
from . import utils


def notificationList(request):
    TEMPLATE = "resources/notifications.html"

    CONTEXT = {
        "notification_list": [],
        "deleted_notifications": [],
    }

    try:
        if not request.user.is_authenticated:
            raise exceptions.PermissionDenied

        if "markall" in request.GET:
            notifications = utils.getNotificationsToList(user=request.user)
            for notification in notifications:
                notification.markNotificationAsRead()

        if "markread" in request.GET:
            notification_id = request.GET["markread"]
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.markNotificationAsRead()

        if "markunread" in request.GET:
            notification_id = request.GET["markunread"]
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.markNotificationAsUnread()

        if "restorenotification" in request.GET:
            notification_id = request.GET["restorenotification"]
            notification = resource_models.Notification.objects.get(id=notification_id)
            notification.restoreNotification()

        if request.method == "POST":
            if "delete" in request.POST:
                notification_id = request.POST["delete"]
                notification = resource_models.Notification.objects.get(
                    id=notification_id
                )
                notification.deleteNotification()

        notification_list = utils.getNotificationsToList(user=request.user)
        deleted_notifications = utils.getDeletedNotifications(user=request.user)

        CONTEXT["notification_list"] = notification_list
        CONTEXT["deleted_notifications"] = deleted_notifications
    except Exception:
        print("Permission Denied")
        return HttpResponseNotFound("Oops, page not found")

    return render(request, TEMPLATE, CONTEXT)
