# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from common_controller.util import http_response_by_json
from motion9 import const
from users.models import Purchase, BeforePayment, Payment


# 배송 관련한 admin page이다
# 배송상태를 확인하고, 배송정보를 입력할 수 있다.
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


# payment상태를 update하는 api이다
# status( 배송대기, 배송중 등등...)과 송장번호(shipping_number)를 update한다.
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

# Purchase관련 내용을 입력하는 Api이다.
# 예를 들어 어떤 사용자가 어떤 상품을 몇개를 샀는지 같은 정보를 입력하는데 사용한다
class PurchaseUpdateView(UpdateView):
    model = Purchase
    # fields = ['user', 'payment', 'price', 'product',]
    template_name = 'update/basic.html'

    def get_success_url(self):
        return reverse_lazy('foradmin:manage_shipping', args=[])

# 위에서는 purchase관련 내용을 입력했으면 이곳에선 payment관련 내용을 입력한다.
# 위의 Purchase에서 사용한 Payment를 입력한다. 예를 들어 상품을 사는데 무슨 결제수단으로 얼마를 결제했는지 등 이다.
class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = 'update/basic.html'

    def get_success_url(self):
        return reverse_lazy('foradmin:manage_shipping', args=[])