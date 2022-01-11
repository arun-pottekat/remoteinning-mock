from datetime import datetime

from django.contrib import messages
from django.shortcuts import render
from django.views import View

from remoteinning import constants
from resources import utils


class HomeView(View):
    template_name = "pages/home.html"

    def set_notification_data(self, header, message):
        notification_data = {}
        notification_data["header"] = header
        notification_data["message"] = message
        return notification_data

    def create_payment_success(self, request, user):
        header = "Payment Successful"
        message = "Payment for 100Rs has been made successfully on {}".format(
            datetime.now()
        )

        notification_data = self.set_notification_data(header, message)
        notification = utils.create_notification(notification_data)
        if notification:
            notification.set_notification_status(constants.NOTIFICATION_SUCCESS)
            notification.set_notification_users(user, user)
            messages.success(request, "Payment successful notification generated")

        return

    def create_payment_failure(self, request, user):
        header = "Payment Failed"
        message = "Payment for 100Rs failed on {}".format(datetime.now())

        notification_data = self.set_notification_data(header, message)
        notification = utils.create_notification(notification_data)
        if notification:
            notification.set_notification_status(constants.NOTIFICATION_DANGER)
            notification.set_notification_users(user, user)
            messages.error(request, "Payment failed notification generated")

        return

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        if "paymentsuccess" in request.POST:
            self.create_payment_success(request, request.user)
        elif "paymentfailure" in request.POST:
            self.create_payment_failure(request, request.user)

        return render(request, self.template_name, {})
