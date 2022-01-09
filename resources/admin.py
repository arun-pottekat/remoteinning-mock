from django.contrib import admin

from resources import models as resource_models


# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(resource_models.Notification, NotificationAdmin)
