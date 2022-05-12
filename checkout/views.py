from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import View
from user.models import Customer
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from product.models import Order
from django.views.decorators.csrf import csrf_exempt


class PaymentView(View):
    def get(self, request, **kwargs):
        total = self.kwargs['price']
        pk = self.kwargs['pk']

        if float(total) > 0:
            order = get_object_or_404(Order, id=pk)
            print(order)
            host = request.get_host()

            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': '%.2f' % float(total),
                'item_name': 'Order {}'.format(order.id),
                'invoice': str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host,
                                                   reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,
                                                   reverse('checkout:payment_done')),
                'cancel_return': 'http://{}{}'.format(host,
                                                      reverse('checkout:payment_cancelled')),
            }

            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'checkout/main.html', {'order': order, 'form': form})
        else:
            return render(request, 'checkout/error.html')


@csrf_exempt
def payment_done(request):
    pk = request.user.pk
    customer = Customer.objects.get(pk=pk)
    order = Order.objects.get(customer=customer, complete=False)
    order.complete = True
    order.save()
    return render(request, 'checkout/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'checkout/payment_cancelled.html')
