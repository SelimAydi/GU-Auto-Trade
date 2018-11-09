from django.conf import settings

from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):
    # def is_open_order(self):
    #     print('is open payment: ', self.status == settings.ORDER_OPEN_STATUS)
    #     return self.status == settings.ORDER_OPEN_STATUS

    def is_failed_order(self):
        print('Order failed: ', self.status == settings.ORDER_FAILED_STATUS)
        return self.status == settings.ORDER_FAILED_STATUS

    def is_paid_order(self):
        print('Order paid: ', self.status == settings.ORDER_PAID_STATUS)
        return self.status == settings.ORDER_PAID_STATUS

    def is_cancelled_order(self):
        print('Order cancelled: ', self.status == settings.ORDER_CANCELLED_STATUS)
        return self.status == settings.ORDER_CANCELLED_STATUS



from oscar.apps.order.models import *
