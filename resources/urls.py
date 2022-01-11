from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path(
        "notifications/",
        login_required(views.NotificationListView.as_view()),
        name="notifications",
    ),
]
