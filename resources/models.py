from django.db import models
from django.utils.translation import gettext_lazy as _

from remoteinning import constants


class Notification(models.Model):
    NOTIFICATION_STATUS = (
        (constants.NOTIFICATION_SUCCESS, "Success"),
        (constants.NOTIFICATION_DANGER, "Danger"),
        (constants.NOTIFICATION_WARNING, "Warning"),
        (constants.NOTIFICATION_INFO, "Info"),
    )

    from_user = models.ForeignKey(
        "users.User",
        related_name="notification_from",
        verbose_name=_("Notification From"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    to_user = models.ForeignKey(
        "users.User",
        related_name="notification_to",
        verbose_name=_("Notification To"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    header = models.CharField(_("Notification heading"), max_length=50)
    message = models.CharField(
        _("Notification message"), max_length=250, blank=True, null=True
    )

    status = models.CharField(
        _("Notification Status"), max_length=10, choices=NOTIFICATION_STATUS
    )

    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    mark_read = models.BooleanField(_("Mark as Read"), default=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return "{}: {}".format(self.status, self.header)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = [
            "-created_on",
        ]

    def setNotificationStatus(self, status):
        self.status = status
        self.save()
        return True

    def setNotificationUsers(self, from_user=None, to_user=None):
        if from_user:
            self.from_user = from_user

        if to_user:
            self.to_user = to_user

        self.save()
        return True

    def deleteNotification(self):
        self.is_deleted = True
        self.save()
        return True

    def restoreNotification(self):
        self.is_deleted = False
        self.save()
        return True

    def markNotificationAsRead(self):
        self.mark_read = True
        self.save()
        return True

    def markNotificationAsUnread(self):
        self.mark_read = False
        self.save()
        return True
