from resources import models as resource_models


def create_notification(notification_data):
    try:
        notification = resource_models.Notification.objects.create(**notification_data)
        return notification
    except Exception:
        return None


def get_notifications_to_list(user):
    notifications = resource_models.Notification.objects.filter(
        to_user=user, is_deleted=False
    )

    return notifications


def get_deleted_notifications(user):
    notifications = resource_models.Notification.objects.filter(
        to_user=user, is_deleted=True
    )

    return notifications
