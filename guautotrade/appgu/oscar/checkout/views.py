import logging

from django.utils import six
from django import http

from django import http
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import six
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.views import generic

from oscar.apps.checkout import views as oscar_views
from oscar.apps.payment.models import Source
from oscar.core.loading import get_class, get_classes, get_model
# from oscar.apps.payment.exceptions import RedirectRequired
from oscar.apps.checkout import signals

from mollie_oscar.facade import Facade

logger = logging.getLogger('oscar.checkout')
ShippingAddressForm, ShippingMethodForm, GatewayForm \
    = get_classes('checkout.forms', ['ShippingAddressForm', 'ShippingMethodForm', 'GatewayForm'])
OrderCreator = get_class('order.utils', 'OrderCreator')
UserAddressForm = get_class('address.forms', 'UserAddressForm')
Repository = get_class('shipping.repository', 'Repository')
AccountAuthView = get_class('customer.views', 'AccountAuthView')
RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
NoShippingRequired = get_class('shipping.methods', 'NoShippingRequired')
Order = get_model('order', 'Order')
ShippingAddress = get_model('order', 'ShippingAddress')
CommunicationEvent = get_model('order', 'CommunicationEvent')
PaymentEventType = get_model('order', 'PaymentEventType')
PaymentEvent = get_model('order', 'PaymentEvent')
UserAddress = get_model('address', 'UserAddress')
Basket = get_model('basket', 'Basket')
Email = get_model('customer', 'Email')
Country = get_model('address', 'Country')
CommunicationEventType = get_model('customer', 'CommunicationEventType')

class PaymentDetailsView(oscar_views.PaymentDetailsView):
    def handle_payment(self, order_number, total, submission):
        # submission = kwargs['submission']

        # Create new Mollie Payment!
        facade = Facade()
        payment_id = facade.create_payment(order_number=order_number,
                                           total=total.incl_tax,
                                           redirect_url=self.get_success_url())

        # Register the Oscar Source(Type)
        source = Source(
            source_type=facade.get_source_type(),
            amount_allocated=total.incl_tax,
            currency=total.currency,
            reference=payment_id
        )
        self.add_payment_source(source)

        # Record Payment event and create the Order(!)
        self.add_payment_event('pre-auth', total.incl_tax)
        self._save_order(order_number, submission)

        # Redirect to Mollie Payment Page
        url = facade.get_payment_url(payment_id)
        raise RedirectRequired(url)

    def _save_order(self, order_number, submission):
        # Oscar by default doesn't create an order after a RedirectRequired raise.
        # Overrule this by creating an Order before raising using this copy-pasted method
        # from the Oscar package.
        logger.info(u"Order #%s: payment started, placing order", order_number)
        print(submission)
        try:
            return self.handle_order_placement(
                order_number, submission['user'],
                submission['basket'],
                submission['shipping_address'],
                submission['shipping_method'],
                submission['shipping_charge'],
                submission['billing_address'],
                submission['order_total']
                # **(submission['order_kwargs'])
            )
        except oscar_views.UnableToPlaceOrder as e:
            logger.error(u"Order #%s: unable to place order - %s", order_number, e, exc_info=True)
            msg = six.text_type(e)
            self.restore_frozen_basket()
            return self.render_to_response(self.get_context_data(error=msg))

    def send_confirmation_message(self, order, code, **kwargs):
        # Don't send the confirmation message before we know the Order is paid for.
        pass

    def submit(self, user, basket, shipping_address, shipping_method,
        shipping_charge, billing_address, order_total,
        payment_kwargs=None, order_kwargs=None):

        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission process for basket #%d",
                    order_number, basket.id)

        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        submission = {
            'user': user,
            'basket': basket,
            'shipping_address': shipping_address,
            'shipping_method': shipping_method,
            'shipping_charge': shipping_charge,
            'billing_address': billing_address,
            'order_total': order_total,
            'order_number': order_number
        }

        try:
            print('Handling payment...')
            self.handle_payment(order_number, order_total, submission)
        except RedirectRequired as e:
            # Redirect required (eg PayPal, 3DS)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return http.HttpResponseRedirect(e.url)
        except UnableToTakePayment as e:
            msg = six.text_type(e)
            logger.warning(
                "Order #%s: unable to take payment (%s) - restoring basket",
                order_number, msg)
            self.restore_frozen_basket()

            return self.render_payment_details(
                self.request, error=msg, **payment_kwargs)
        except PaymentError as e:
            # A general payment error - Something went wrong
            msg = six.text_type(e)
            logger.error("Order #%s: payment error (%s)", order_number, msg,
                         exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.error(
                "Order #%s: unhandled exception while taking payment (%s)",
                order_number, e, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)

        signals.post_payment.send_robust(sender=self, view=self)

        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment successful, placing order",
                    order_number)
        try:
            return self.handle_order_placement(
                order_number, user, basket, shipping_address, shipping_method,
                shipping_charge, billing_address, order_total, **order_kwargs)
        except UnableToPlaceOrder as e:
            msg = six.text_type(e)
            logger.error("Order #%s: unable to place order - %s",
                         order_number, msg, exc_info=True)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=msg, **payment_kwargs)
