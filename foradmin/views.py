# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from common_controller.util import http_response_by_json
from motion9 import const
from users.models import Purchase, BeforePayment, Payment


def manage_shipping_view(request):
    if request.user.is_superuser:

        purchases = Purchase.objects.all()
        for purchase in purchases:
            if purchase.type == 'p':
                purchase.item_name = purchase.product.name
            elif purchase.type == 's':
                purchase.item_name = purchase.set.name
            elif purchase.type == 'c':
                purchase.item_name = 'Custom!'

            if purchase.payment.status == 'b':
                purchase.payment.status_name = '상품 준비중'
            elif purchase.payment.status == 'r':
                purchase.payment.status_name = '배송대기'
            elif purchase.payment.status == 's':
                purchase.payment.status_name = '배송중'
            elif purchase.payment.status == 'f':
                purchase.payment.status_name = '배송완료'

            purchase.new_mileage = int(purchase.payment.auth_amount)/100

        return render(request, 'manage_shipping.html', {
            'purchases':purchases
        } )


    else:
        return HttpResponse('is not superuser!')

@csrf_exempt
def payment_update(request, pk):
    status = request.POST.get('status',None )
    shipping_number = request.POST.get('shipping_number',None )

    if status is None or shipping_number is None:
        pass
    else:
        if request.user.is_superuser:
            Payment.objects.filter(pk=pk).update(status=status, shipping_number=shipping_number)
            return http_response_by_json(None)
        else:
            pass

    return http_response_by_json(const.CODE_PARAMS_WRONG)


class PurchaseUpdateView(UpdateView):
    model = Purchase
    # fields = ['user', 'payment', 'price', 'product',]
    template_name = 'update/basic.html'

    def get_success_url(self):
        return reverse_lazy('foradmin:manage_shipping', args=[])

class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = 'update/basic.html'

    def get_success_url(self):
        return reverse_lazy('foradmin:manage_shipping', args=[])