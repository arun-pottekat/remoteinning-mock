from resources import models as resource_models


def createNotification(notification_data):
    try:
        notification = resource_models.Notification.objects.create(**notification_data)
        return notification
    except Exception:
        return None


def getNotification(notification_id):
    return resource_models.Notification.objects.get(id=notification_id)


def getNotificationsToList(user):
    notifications = resource_models.Notification.objects.filter(
        to_user=user, is_deleted=False
    )

    return notifications


def getDeletedNotifications(user):
    notifications = resource_models.Notification.objects.filter(
        to_user=user, is_deleted=True
    )

    return notifications
