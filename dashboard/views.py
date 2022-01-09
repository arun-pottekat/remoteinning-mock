from datetime import datetime

from django.contrib import messages
from django.shortcuts import render

from remoteinning import constants
from resources import utils


def home(request):
    TEMPLATE = "pages/home.html"

    try:
        notification_data = {}
        if "paymentsuccess" in request.POST:
            notification_data["header"] = "Payment Successful"
            notification_data[
                "message"
            ] = "Payment for 100Rs has been made successfully on {}".format(
                datetime.now()
            )
            notification = utils.createNotification(notification_data)
            if notification:
                notification.setNotificationStatus(constants.NOTIFICATION_SUCCESS)
                notification.setNotificationUsers(request.user, request.user)
                messages.success(request, "Payment successful notification generated")

        if "paymentfailure" in request.POST:
            notification_data["header"] = "Payment Failed"
            notification_data["message"] = "Payment for 100Rs failed on {}".format(
                datetime.now()
            )
            notification = utils.createNotification(notification_data)
            if notification:
                notification.setNotificationStatus(constants.NOTIFICATION_DANGER)
                notification.setNotificationUsers(request.user, request.user)
                messages.error(request, "Payment failure notification generated")
    except Exception as e:
        print(e)

    return render(request, TEMPLATE)
