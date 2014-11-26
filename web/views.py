#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.request import RAISE_ERROR
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template import Context
from common_controller import util
from foradmin.models import MainImage, Advertisement, Preference
from motion9 import settings

from motion9.const import *
from common_controller.util import helper_get_user, helper_get_product_detail, helper_get_set, helper_make_paging_data, \
    http_response_by_json, helper_get_products, helper_get_set_list, helper_get_blog_reviews, \
    helper_get_custom_set, helper_get_custom_set_list, helper_get_brands, helper_get_product_magazines, \
    helper_add_custom_set_cart, helper_get_adarea_items, helper_get_faq_items, helper_get_survey_items, \
    helper_get_survey_list
from .models import Product, Category, BlogReview, Set, Brand
from users.models import CustomSet, CustomSetDetail, Payment, Cart, Purchase, OrderTempInfo, BeforePayment

from subprocess import call, Popen, PIPE
import urllib
import time
import json
import logging
from web.models import Faq

logger = logging.getLogger(__name__)

@csrf_exempt
def test_view(request):

    http_user_agent = request.META.get('HTTP_USER_AGENT').lower()
    # print request.META.get('HTTP_REFERER')


    return HttpResponse('success!')
    # return render(request, 'payment_complete_web.html')
    # return render(request, 'uservoice_test.html')

@csrf_exempt
@login_required
def before_payment(request):

    print request.POST

    order_id = request.POST.get('order_id', '')

    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    postcode = request.POST.get('postcode', '')
    basic_address = request.POST.get('basic_address', '')
    detail_address = request.POST.get('detail_address', '')
    shipping_requirement = request.POST.get('shipping_requirement', '')
    mileage = request.POST.get('mileage', '')
    if len(mileage)==0:
        mileage=0

    try:
        BeforePayment.objects.create(
            user=request.user,
            order_id=order_id,
            name=name,
            phone=phone,
            postcode=postcode,
            address=basic_address+' '+detail_address,
            shipping_requirement=shipping_requirement,
            mileage=mileage
        )
        return http_response_by_json()

    except Exception as e:
        return http_response_by_json( CODE_PARAMS_WRONG )


@csrf_exempt
def payment_return_view(request):

    service_id = request.POST.get('SERVICE_ID')
    order_id = request.POST.get('ORDER_ID')
    order_date = request.POST.get('ORDER_DATE')
    post_response_code = request.POST.get('RESPONSE_CODE')
    check_sum = request.POST.get('CHECK_SUM')
    http_user_agent = request.META.get('HTTP_USER_AGENT').lower()
    if http_user_agent.find('firefox') == -1 and http_user_agent.find('chrome') == -1 and \
                    http_user_agent.find('safari') == -1 and http_user_agent.find('opera') == -1:
        message = request.POST.get('MESSAGE')
    else:
        message = urllib.unquote_plus(request.POST.get('MESSAGE'))

    is_success = False

    if post_response_code == "0000":
        temp = service_id+order_id+order_date
        checksum_command = 'java -cp ./libs/jars/billgateAPI.jar com.galaxia.api.util.ChecksumUtil ' + 'DIFF ' + check_sum + " " + temp
        checksum = (Popen(checksum_command.split(' '), stdout=PIPE).communicate()[0]).strip()
        if checksum == 'SUC':
            credit_card_service_code = '0900'
            broker_message_command = ["java","-Dfile.encoding=euc-kr","-cp","./libs/jars/billgateAPI.jar","com.galaxia.api.EncryptServiceBroker","./libs/config/config.ini",credit_card_service_code, message]
            return_message = (Popen(broker_message_command, stdout=PIPE).communicate()[0]).strip()
            return_code = return_message[0:5]

            this_data = {}
            if return_code=='ERROR':
                this_version = "0100"
                this_merchantId = service_id
                this_serviceCode = credit_card_service_code
                this_command = "3011"
                this_orderId = order_id
                this_orderDate = order_date

                util.billgate_put_data(this_data, "1002", return_message[6:10])
                util.billgate_put_data(this_data, "1003", "API error!!")
                util.billgate_put_data(this_data, "1009", return_message[10:12])
                util.billgate_put_data(this_data, "1010", util.billgate_getErrorMessage(return_message[6:12]))
            else:
                # {{ Message.php

                set_data_param = return_message
                VERSION_LENGTH = 10
                MERCHANT_ID_LENGTH = 20
                SERVICE_CODE_LENGTH = 4
                COMMAND_LENGTH = 4
                ORDER_ID_LENGTH = 64
                DATE_LENGTH = 14
                TAG_LENGTH = 4
                COUNT_LENGTH = 4
                VALUE_LENGTH = 4

                VERSION_INDEX = 0
                MERCHANT_ID_INDEX = 10
                SERVICE_CODE_INDEX = 30

                COMMAND_INDEX = 0
                ORDER_ID_INDEX = 4
                ORDER_DATE_INDEX = 68
                DATA_INDEX = 82

                this_version = set_data_param[VERSION_INDEX:VERSION_INDEX+VERSION_LENGTH].strip()
                this_merchantId = set_data_param[MERCHANT_ID_INDEX:MERCHANT_ID_INDEX+MERCHANT_ID_LENGTH].strip()
                this_serviceCode = set_data_param[SERVICE_CODE_INDEX:SERVICE_CODE_INDEX+SERVICE_CODE_LENGTH].strip()

                decrypted = set_data_param[VERSION_LENGTH+MERCHANT_ID_LENGTH+SERVICE_CODE_LENGTH:VERSION_LENGTH+MERCHANT_ID_LENGTH+SERVICE_CODE_LENGTH+len(set_data_param)]

                this_command = decrypted[COMMAND_INDEX:COMMAND_INDEX+COMMAND_LENGTH].strip()
                this_orderId = decrypted[ORDER_ID_INDEX:ORDER_ID_INDEX+ORDER_ID_LENGTH].strip()
                this_orderDate = decrypted[ORDER_DATE_INDEX:ORDER_DATE_INDEX+DATE_LENGTH].strip()

                bodyStr = decrypted[DATA_INDEX:DATA_INDEX+len(decrypted)].strip()
                #this->parseData($bodyStr);
                parse_data_param = bodyStr
                arrData = parse_data_param.split("|")
                for i in range(len(arrData)):
                    if len(arrData[i]) != 0:
                        arrValueData = arrData[i].split("=")
                        tag = arrValueData[0]
                        value = arrValueData[1]

                        if this_data.has_key(tag):
                            vt = this_data.get(tag)
                        else:
                            vt = []

                        vt.append(value)
                        this_data[tag] = vt
                # Message.php }}

            response_code = this_data.get('1002')[0]
            response_message = this_data.get('1003')

            detail_response_code = this_data.get('1009')
            detail_response_message = this_data.get('1010')

            if response_code == '0000':
                auth_amount = this_data.get('1007')
                transaction_id = this_data.get('1001')
                auth_date = this_data.get('1005')

                is_success = True

    try:
        response_message = map( lambda x: x.decode('euc-kr'), response_message)
        detail_response_message = map( lambda x: x.decode('euc-kr'), detail_response_message)
    except:
        pass

    if is_success:
        beforePayment = BeforePayment.objects.get(order_id=order_id)
        if beforePayment is None:
            raise Http404

        user_ = beforePayment.user
        user_profile = user_.profile

        payment = Payment.objects.create(
            user=user_,
            service_id=service_id,
            order_id=beforePayment.order_id,
            order_date=order_date,
            transaction_id=transaction_id[0],
            auth_amount=auth_amount[0],
            auth_date=auth_date[0],
            response_code=response_code,
            response_message=response_message[0],
            detail_response_code=detail_response_code[0],
            detail_response_message=detail_response_message[0],
            name= beforePayment.name,
            postcode = beforePayment.postcode,
            phone= beforePayment.phone,
            address= beforePayment.address,
            shipping_requirement= beforePayment.shipping_requirement,
            mileage= beforePayment.mileage
        )

        user_profile.mileage = int(user_profile.mileage)-int(beforePayment.mileage)+int(auth_amount[0])/100
        user_profile.save()

        carts = Cart.objects.filter(order_id=order_id).all()
        for cart in carts:

            if cart.type=='p':
                price = cart.product.discount_price
            elif cart.type=='s':
                price = helper_get_set(cart.set).get('discount_price', 0)
            elif cart.type=='c':
                price = helper_get_custom_set(cart.custom_set).get('discount_price', 0)

            Purchase.objects.create(
                user=user_,
                payment=payment,
                price=price,
                product=cart.product,
                set=cart.set,
                custom_set=cart.custom_set,
                type=cart.type,
                item_count=cart.item_count
            )

        if payment is not None:
            payment_id = payment.id

        Cart.objects.filter(order_id=order_id).delete()

    if http_user_agent.find('firefox') == -1 and http_user_agent.find('chrome') == -1 and \
                    http_user_agent.find('safari') == -1 and http_user_agent.find('opera') == -1:
        return render(request, 'return_explorer.html', {
            'payment_id': payment_id,
            'message': message,
            'return_message': return_message,
            'is_success': is_success,
            'service_id': service_id,
            'order_id': order_id,
            'order_date': order_date,
            'transaction_id': transaction_id,
            'auth_amount': auth_amount,
            'auth_date': auth_date,
            'response_code': response_code,
            'response_message': response_message,
            'detail_response_code': detail_response_code,
            'detail_response_message': detail_response_message
        })
    else:
        if is_success:
            return redirect('payment_complete', payment_id=payment_id )
        else:
            raise Http404

@csrf_exempt
def payment_return_mobile_web_view(request):
    transaction_id = None
    auth_amount = None
    auth_date = None
    response_code = None
    response_message = None
    detail_response_code = None
    detail_response_message = None

    service_id = request.POST.get('SERVICE_ID')
    order_id = request.POST.get('ORDER_ID')
    order_date = request.POST.get('ORDER_DATE')
    post_response_code = request.POST.get('RESPONSE_CODE')
    check_sum = request.POST.get('CHECK_SUM')
    message = request.POST.get('MESSAGE')

    is_success = False

    if post_response_code == "0000":
        credit_card_service_code = '0900'
        broker_message_command = ["java","-Dfile.encoding=euc-kr","-cp","./libs/jars/billgateAPI.jar","com.galaxia.api.EncryptServiceBroker","./libs/config/config.ini", credit_card_service_code, message]
        return_message = Popen(broker_message_command, stdout=PIPE).communicate()[0].strip()
        return_code = return_message[0:5]

        this_data = {}
        if return_code=='ERROR':
            this_version = "0100"
            this_merchantId = service_id
            this_serviceCode = credit_card_service_code
            this_command = "3011"
            this_orderId = order_id
            this_orderDate = order_date

            util.billgate_put_data(this_data, "1002", return_message[6:10])
            util.billgate_put_data(this_data, "1003", "API error!!")
            util.billgate_put_data(this_data, "1009", return_message[10:12])
            util.billgate_put_data(this_data, "1010", util.billgate_getErrorMessage(return_message[6:12]))
        else:
            # {{ Message.php

            set_data_param = return_message
            VERSION_LENGTH = 10
            MERCHANT_ID_LENGTH = 20
            SERVICE_CODE_LENGTH = 4
            COMMAND_LENGTH = 4
            ORDER_ID_LENGTH = 64
            DATE_LENGTH = 14
            TAG_LENGTH = 4
            COUNT_LENGTH = 4
            VALUE_LENGTH = 4

            VERSION_INDEX = 0
            MERCHANT_ID_INDEX = 10
            SERVICE_CODE_INDEX = 30

            COMMAND_INDEX = 0
            ORDER_ID_INDEX = 4
            ORDER_DATE_INDEX = 68
            DATA_INDEX = 82

            this_version = set_data_param[VERSION_INDEX:VERSION_INDEX+VERSION_LENGTH].strip()
            this_merchantId = set_data_param[MERCHANT_ID_INDEX:MERCHANT_ID_INDEX+MERCHANT_ID_LENGTH].strip()
            this_serviceCode = set_data_param[SERVICE_CODE_INDEX:SERVICE_CODE_INDEX+SERVICE_CODE_LENGTH].strip()

            decrypted = set_data_param[VERSION_LENGTH+MERCHANT_ID_LENGTH+SERVICE_CODE_LENGTH:VERSION_LENGTH+MERCHANT_ID_LENGTH+SERVICE_CODE_LENGTH+len(set_data_param)]

            this_command = decrypted[COMMAND_INDEX:COMMAND_INDEX+COMMAND_LENGTH].strip()
            this_orderId = decrypted[ORDER_ID_INDEX:ORDER_ID_INDEX+ORDER_ID_LENGTH].strip()
            this_orderDate = decrypted[ORDER_DATE_INDEX:ORDER_DATE_INDEX+DATE_LENGTH].strip()

            bodyStr = decrypted[DATA_INDEX:DATA_INDEX+len(decrypted)].strip()
            #this->parseData($bodyStr);
            parse_data_param = bodyStr
            arrData = parse_data_param.split("|")
            for i in range(len(arrData)):
                if len(arrData[i]) != 0:
                    arrValueData = arrData[i].split("=")
                    tag = arrValueData[0]
                    value = arrValueData[1]

                    if this_data.has_key(tag):
                        vt = this_data.get(tag)
                    else:
                        vt = []

                    vt.append(value)
                    this_data[tag] = vt
            # Message.php }}

        response_code = this_data.get('1002')[0]
        response_message = this_data.get('1003')

        detail_response_code = this_data.get('1009')
        detail_response_message = this_data.get('1010')

        if response_code == '0000':
            auth_amount = this_data.get('1007')
            transaction_id = this_data.get('1001')
            auth_date = this_data.get('1005')

            is_success = True

    try:
        response_message = map( lambda x: x.decode('euc-kr'), response_message)
        detail_response_message = map( lambda x: x.decode('euc-kr'), detail_response_message)
    except:
        pass

    # payment_id=0

    if is_success:
        beforePayment = BeforePayment.objects.get(order_id=order_id)
        if beforePayment is None:
            raise Http404

        user_ = beforePayment.user
        user_profile = user_.profile

        payment = Payment.objects.create(
            user=user_,
            service_id=service_id,
            order_id=beforePayment.order_id,
            order_date=order_date,
            transaction_id=transaction_id[0],
            auth_amount=auth_amount[0],
            auth_date=auth_date[0],
            response_code=response_code,
            response_message=response_message[0],
            detail_response_code=detail_response_code[0],
            detail_response_message=detail_response_message[0],
            name= beforePayment.name,
            postcode = beforePayment.postcode,
            phone= beforePayment.phone,
            address= beforePayment.address,
            shipping_requirement= beforePayment.shipping_requirement,
            mileage= beforePayment.mileage
        )

        user_profile.mileage = int(user_profile.mileage)-int(beforePayment.mileage)+int(auth_amount[0])/100
        user_profile.save()

        carts = Cart.objects.filter(order_id=order_id).all()
        for cart in carts:

            if cart.type=='p':
                price = cart.product.discount_price
            elif cart.type=='s':
                price = helper_get_set(cart.set).get('discount_price', 0)
            elif cart.type=='c':
                price = helper_get_custom_set(cart.custom_set).get('discount_price', 0)

            Purchase.objects.create(
                user=user_,
                payment=payment,
                price=price,
                product=cart.product,
                set=cart.set,
                custom_set=cart.custom_set,
                type=cart.type,
                item_count=cart.item_count
            )

        if payment is not None:
            payment_id = payment.id

        Cart.objects.filter(order_id=order_id).delete()

    if is_success:
        return redirect('mobile_payment_complete', payment_id=payment_id)
    else:
        return redirect('mobile_mypage_before_purchase')

    # return render(request, 'return_explorer.html', {
    #     'payment_id': payment_id,
    #     'message': message,
    #     'return_message': return_message,
    #     'is_success': is_success,
    #     'service_id': service_id,
    #     'order_id': order_id,
    #     'order_date': order_date,
    #     'transaction_id': transaction_id,
    #     'auth_amount': auth_amount,
    #     'auth_date': auth_date,
    #     'response_code': response_code,
    #     'response_message': response_message,
    #     'detail_response_code': detail_response_code,
    #     'detail_response_message': detail_response_message
    # })

@csrf_exempt
@login_required
def payment_complete_view(request, payment_id=0):
    payment = Payment.objects.get(id=payment_id)

    purchase_products = Purchase.objects.filter(payment_id=payment_id, type='p').all()
    products = []
    for purchase_set in purchase_products:
        product = purchase_set.product
        product_ = helper_get_product_detail(product, request.user)
        product_['item_count'] = purchase_set.item_count
        product_['total_price'] = purchase_set.price
        products.append(product_)

    purchase_sets = Purchase.objects.filter(payment_id=payment_id, type='s').all()
    sets = []
    for purchase_set in purchase_sets:
        set = purchase_set.set
        set_ = helper_get_set(set, request.user)
        set_['item_count'] = purchase_set.item_count
        set_['total_price'] = purchase_set.price
        sets.append(set_)

    purchase_custom_sets = Purchase.objects.filter(payment_id=payment_id, type='c').all()
    custom_sets = []
    for purchase_custom_set in purchase_custom_sets:
        custom_set = purchase_custom_set.custom_set
        custom_set_ = helper_get_custom_set(custom_set, request.user)
        custom_set_['item_count'] = purchase_custom_set.item_count
        custom_set_['total_price'] = purchase_custom_set.price
        custom_sets.append(custom_set_)

    if BeforePayment.objects.filter(order_id=payment.order_id).exists():
        util.send_payment_email(payment_id, request.user)
        BeforePayment.objects.filter(order_id=payment.order_id).delete()

    return render(request, 'payment_complete_web.html', {
        'products': products,
        'sets': sets,
        'custom_sets': custom_sets,
        'payment': payment,
        'user_': request.user
    })

@csrf_exempt
def index_view(request):
    if request.is_mobile:
        return redirect('mobile_index')

    product_categories = Category.objects.filter(is_set=False).all()
    set_categories = Category.objects.filter(is_set=True).all()

    try:
        main_image = settings.MEDIA_URL + MainImage.objects.get(name='main').image.name
    except:
        main_image=''

    set_category_images_row = []
    try:
        set_categorys = Category.objects.filter(is_set=True).all()

        set_category_images = []
        for set_category in set_categorys:
            set_category_images.append( {
                'id': set_category.id,
                'image_url': settings.MEDIA_URL + set_category.small_image.name
            })
            if len(set_category_images) == 3:
                set_category_images_row.append(set_category_images)
                set_category_images = []

        if len(set_category_images) != 0:
            set_category_images_row.append(set_category_images)
    except:
        pass

    main_notice = Preference.objects.filter(name='MainNotice').first()

    return render(request, 'index_web.html',
                  {
                      'product_categories': product_categories,
                      'set_categories': set_categories,
                      'main_image': main_image,
                      'set_category_images_row': set_category_images_row,
                      'next': 'index',
                      'main_notice': main_notice
                  })

@csrf_exempt
def shop_product_view(request, category_id=None, page_num=1):

    page_num = int(page_num)
    price_max_filter = request.GET.get('price_max', None)
    price_min_filter = request.GET.get('price_min', None)
    brandname_filter = request.GET.get('brandname', None)
    products_ = helper_get_products(helper_get_user(request), category_id, price_max_filter, price_min_filter, brandname_filter)

    if page_num is not None:
        products_ = helper_make_paging_data(len(products_), products_[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_FOR_PRODUCT], ITEM_COUNT_PER_PAGE_FOR_PRODUCT, page_num)
    else:
        products_ = {'data': products_}

    # return http_response_by_json(None, products_ )

    categories = Category.objects.filter(is_set=False).all()

    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    brands = helper_get_brands()
    adarea_items = helper_get_adarea_items(request)

    return render(request, 'shopping_product_web.html',
                  {

                      'products': products_,
                      'current_category': current_category,
                      'current_category_id': category_id,
                      'categories': categories,
                      'current_page': 'shop_product',
                      'current_brand': brandname_filter,
                      'brands': brands,
                      'adarea_items': adarea_items
                  })


def shop_set_view(request, category_id=None, page_num=1):

    page_num = int(page_num)
    price_max_filter = request.GET.get('price_max', None)
    price_min_filter = request.GET.get('price_min', None)
    sets = helper_get_set_list(category_id, helper_get_user(request), price_max_filter, price_min_filter)

    if page_num is not None:
        sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_SET:page_num*ITEM_COUNT_PER_PAGE_FOR_SET], ITEM_COUNT_PER_PAGE_FOR_SET, page_num)
    else:
        sets = {'data': sets}

    categories = Category.objects.filter(is_set=True).all()
    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    brands = helper_get_brands()
    adarea_items = helper_get_adarea_items(request)

    # print sets['data'][0].keys()
    # print sets['data'][0]['products']
    # print sets['data'][0]['products'][0]['name']

    return render(request, 'shopping_set_web.html',
                  {
                      'sets': sets,
                      'current_category': current_category,
                      'current_category_id': category_id,
                      'categories': categories,
                      'current_page': 'shop_set',
                      'brands': brands,
                      'adarea_items': adarea_items
                  })

@csrf_exempt
def set_view(request, set_id):
    set = helper_get_set(set_id, helper_get_user(request))

    return render(request, 'set_detail_web.html',
                {
                    'set': set
                })

@csrf_exempt
def product_view(request, product_id=None):
    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))

        product['category_guide_image'] = MainImage.objects.filter(name=product['category_name']).first()
        if product['category_guide_image'] is not None:
            product['category_guide_image'] = settings.MEDIA_URL + product['category_guide_image'].image.name

        blog_reivews = helper_get_blog_reviews(product_id)
        magazines = helper_get_product_magazines(product_id)
        magazines_fold = magazines[4:]
        magazines = magazines[:4]

        return render(request, "product_detail_web.html",
                      {
                          'product': product,
                          'magazines': magazines,
                          'magazines_fold': magazines_fold,
                          'blog_reviews': blog_reivews
                      })
    else:
        return render(request, "404.html")

@csrf_exempt
def product_modal_view(request, product_id=None):
    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))
        blog_reivews = helper_get_blog_reviews(product_id)

        return render(request, "product_detail_for_modal.html",
                      {
                          'product': product,
                          'blog_reviews': blog_reivews
                      })
    else:
        return render(request, "404.html")

@csrf_exempt
def product_json_view(request, product_id=None):
    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))
        return http_response_by_json(None, product)
    else:
        return render(request, "404.html")

@csrf_exempt
def customize_set_make_view(request, set_id):
    set = helper_get_set(set_id, helper_get_user(request), True)

    return render(request, "change_product_in_set_web.html",
          {
              'set': set
          })

@csrf_exempt
def customize_set_view(request):
    if helper_get_user(request) is None:
        return redirect('login_page')

    custom_sets = helper_get_custom_set_list(helper_get_user(request))
    adarea_items = helper_get_adarea_items(request)

    return render(request, "shopping_custom_web.html",
          {
              'custom_sets': custom_sets,
              'adarea_items': adarea_items
          })

    # set =

@csrf_exempt
def customize_set_detail_view(request, set_id):
    custom_set = helper_get_custom_set(set_id, helper_get_user(request))

    return render(request, "custom_detail_web.html",
          {
              'custom_set': custom_set
          })

@csrf_exempt
def customize_set_save_view(request):
    user = helper_get_user(request)
    data = request.POST.get('data', None)
    will_added = request.POST.get('addToCart', False)

    post_json = json.loads(data)
    set_id = post_json.get('set_id')
    custom_list = post_json.get('custom_lists')

    if set_id is None:
        return HttpResponse('is error')

    if user is not None:
        custom_set, is_created = CustomSet.objects.get_or_create(user=user, set_id=set_id)
        if not(is_created):
            Cart.objects.filter(custom_set=custom_set).delete()

        for custom_item in custom_list:
            original_id = custom_item.get('original_id')
            new_id = custom_item.get('new_id')
            if CustomSetDetail.objects.filter(custom_set=custom_set, original_product_id=original_id).exists():
                CustomSetDetail.objects.filter(custom_set=custom_set, original_product_id=original_id).update(new_product=new_id)
            else:
                CustomSetDetail.objects.create(custom_set=custom_set, original_product_id=original_id, new_product_id=new_id)

        if will_added:
            helper_add_custom_set_cart(user, custom_set.id)
        return http_response_by_json()
    else:
        return http_response_by_json(CODE_LOGIN_REQUIRED)


@csrf_exempt
def help_faq_view(request):
    faqs = helper_get_faq_items(request)
    return render(request, 'help_faq.html', {
        'faqs':faqs
    })

@login_required
def report_view(request, category_id=None, page_num=1):

    user = helper_get_user(request)
    user_profile = user.profile
    page_num = int(page_num)
    price_max_filter = request.GET.get('price_max', None)
    price_min_filter = request.GET.get('price_min', None)
    brandname_filter = request.GET.get('brandname', None)
    products_ = helper_get_products(helper_get_user(request), category_id, price_max_filter, price_min_filter, brandname_filter)

    if page_num is not None:
        products_ = helper_make_paging_data(len(products_), products_[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_FOR_PRODUCT], ITEM_COUNT_PER_PAGE_FOR_PRODUCT, page_num)
    else:
        products_ = {'data': products_}

    # return http_response_by_json(None, products_ )

    categories = Category.objects.filter(is_set=False).all()

    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    brands = helper_get_brands()
    adarea_items = helper_get_adarea_items(request)
    phone = user_profile.phone
    phones = phone.split("-")
    phone1 = phone2 = phone3 = ''

    if user is not None:

        return render(request, 'report_web.html',
            {
                'products': products_,
                'current_category': current_category,
                'current_category_id': category_id,
                'categories': categories,
                'current_page': 'shop_product',
                'current_brand': brandname_filter,
                'brands': brands,
                'adarea_items': adarea_items,
                'tab_name': 'myinfo',
                'next': next
            })

    else:
        logger.error('have_to_login')


@login_required
def report_detail_modal_view(request, category_id=None, page_num=1, product_id=None):

    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))
        blog_reivews = helper_get_blog_reviews(product_id)

        return render(request, "product_detail_for_modal.html",
                      {
                          'product': product,
                          'blog_reviews': blog_reivews
                      })
    else:
        return render(request, "404.html")


@csrf_exempt
def report_form_index_view(request):

    return render(request, 'report_form_index_web.html',
                  {
                      'next': reverse('report_form'),
                  })

@login_required
def report_form_view(request):
    survey = helper_get_survey_items(request)

    survey_ = []
    survey_group = []
    survey_range = len(survey['survey_items']) + 1

    for i in range(len(survey['survey_items'])):
        survey['survey_items'][i].update({
            'label_index': str(i + 1)
        })
        survey_group.append(survey['survey_items'][i])
        if (i + 1) % 3 == 0:
            survey_.append(survey_group)
            survey_group = []

    if len(survey_group) != 0:
        survey_.append(survey_group)

    return render(request, 'report_form_web.html',
                  {
                      'next': reverse('report_form'),
                      'survey': survey_,
                      'survey_id': survey['survey_id'],
                      'survey_range': survey_range
                  })

@login_required
def survey_list_in_json(request):
    survey_list = helper_get_survey_list(request)

    for item in survey_list:
        item['created'] = item['created'].strftime("%Y %m %d")

    return HttpResponse(json.dumps({'data': list(survey_list)}, ensure_ascii=False), content_type="application/json; charset=utf-8")