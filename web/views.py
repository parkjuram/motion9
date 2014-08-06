#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from common_controller import util

from motion9.const import *
from common_controller.util import helper_get_user, helper_get_product_detail, helper_get_set, helper_make_paging_data, \
    http_response_by_json, helper_get_products, helper_get_set_list, helper_get_blog_reviews, \
    helper_get_custom_set, helper_get_custom_set_list, helper_get_brands
from .models import Product, Category, BlogReview, Set, Brand
from users.models import CustomSet, CustomSetDetail, Payment

from subprocess import call, Popen, PIPE
import urllib
import time
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def test_view(request):

    # products = Product.objects.all()
    # for product in products:
    #     product.short_desc = product.description
    #     product.save()

    return HttpResponse('success!')

    # return render(request, 'payment_complete_web.html')

    # return render(request, 'uservoice_test.html')

@csrf_exempt
def payment_pay_chrome_view(request):
    pass
    # current_datetime = time.strftime("%Y%m%d%H%M%S")
    # service_id = 'glx_api'
    # order_date = current_datetime
    # order_id = 'arsdale_' + order_date
    # amount = '1000'
    #
    # # checksum
    # temp = service_id+order_id+amount
    # checksum_command = 'java -cp ./libs/jars/billgateAPI.jar com.galaxia.api.util.ChecksumUtil ' + \
    #     'GEN ' + temp
    #
    # checksum = Popen(checksum_command.split(' '), stdout=PIPE).communicate()[0]
    # checksum = checksum.strip()
    #
    # if checksum=='8001' or checksum=='8003' or checksum=='8009':
    #     return HttpResponse('error code : '+checksum+' \nError Message: make checksum error! Please contact your system administrator!')
    #
    # return render(request, 'pay_explorer.html', {
    #     'service_id': service_id,
    #     'order_id': order_id,
    #     'order_date': order_date,
    #     'user_id': user_id,
    #     'item_code': 'TEST_CD1',
    #     'using_type': '0000',
    #     'currency': '0000',
    #     'item_name': item_name,
    #     'amount': amount,
    #     'user_ip': user_ip,
    #     'installment_period': '0:3',
    #     'return_url': return_url,
    #     'check_sum': checksum
    # })

@csrf_exempt
def payment_pay_explore_view(request):
    current_datetime = time.strftime("%Y%m%d%H%M%S")

    # testing option
    service_id = 'glx_api'
    order_date = current_datetime
    order_id = 'arsdale_' + order_date
    user_id = 'arsdale@naver.com'
    user_name = 'arsdale'
    item_name = 'beyond_sun_2014'
    item_code = '01_01_2014'
    amount = '1000'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    return_url = request.build_absolute_uri(reverse('payment_return_explore'))


    # checksum
    temp = service_id+order_id+amount
    checksum_command = 'java -cp ./libs/jars/billgateAPI.jar com.galaxia.api.util.ChecksumUtil ' + \
        'GEN ' + temp

    checksum = Popen(checksum_command.split(' '), stdout=PIPE).communicate()[0]
    checksum = checksum.strip()

    print checksum

    if checksum=='8001' or checksum=='8003' or checksum=='8009':
        return HttpResponse('error code : '+checksum+' \nError Message: make checksum error! Please contact your system administrator!')


    return render(request, 'pay_explorer.html', {
        'service_id': service_id,
        'order_id': order_id,
        'order_date': order_date,
        'user_id': user_id,
        'item_code': 'TEST_CD1',
        'using_type': '0000',
        'currency': '0000',
        'item_name': item_name,
        'amount': amount,
        'user_ip': user_ip,
        'installment_period': '0:3',
        'return_url': return_url,
        'check_sum': checksum
    })


@csrf_exempt
def payment_return_openbrowser(request):

    is_success = None
    service_id = None
    order_id = None
    order_date = None
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
    message = urllib.unquote_plus(message)

    is_success = False

    if post_response_code == "0000":
        temp = service_id+order_id+order_date
        checksum_command = 'java -cp ./libs/jars/billgateAPI.jar com.galaxia.api.util.ChecksumUtil ' + \
        'DIFF ' + check_sum + " " + temp
        checksum = Popen(checksum_command.split(' '), stdout=PIPE).communicate()[0]
        checksum = checksum.strip()
        if checksum == 'SUC':


    # #         # function ServiceBroker('java -Dfile.encoding=euc-kr -cp ./libs/jars/billgateAPI.jar com.galaxia.api.EncryptServiceBroker',
    # #         #  './libs/config/config.ini')
    #         bin = 'java -Dfile.encoding=euc-kr -cp ./libs/jars/billgateAPI.jar com.galaxia.api.EncryptServiceBroker '
    #         config_file = '"/Users/ramju/Documents/workspace/django/project_motion9/motion9/libs/config/config.ini"'
    #         service_code = '"0900"'
    #         broker_message_command = bin+' '+config_file+' '+service_code+' "'+message + '"';
    #         print broker_message_command
    #         return_message = Popen(["java","-Dfile.encoding=euc-kr","-cp","./libs/jars/billgateAPI.jar","com.galaxia.api.EncryptServiceBroker","./libs/config/config.ini","0900","07180100      glx_api             0900y4w2jWCkhK6+7CTywaME87rUuYBO/yNgXErm0CgTv1GKQmU3eQvB+cGoFgo/w5R0hAiXS80Pcifm03Cen8rcbjR+46fB1uVPCFkB//Ois0jyJsSR9SN2Hr9C20EylIYSGc3uue86jc7G2L91ocZec7Y0JaiQZ6Qc6AdC/WxvPPueE0EzT4gx+mIAcCpMEBKdPtsCk+/Gcj2tXziqEM0HuumMgWtZI6ffhxQJNc/LuRpb6lM+JSPcO3eilE3XcQgtLWbkPeYduceVnRoaMG0fmec6Bhyy7HcjXiYTEG432G08KoaFPDXCUJp0anqlRjwzGo1w2h7+SFvTync32Bw1x195YR1I3biKGhvhS9iglgZ2Gb1TP8cZBdhZvCXqTMiUqEIRo2cKsqjHenfn4bAHvNrmOBeixCkcVHtnKtTEN26A4Cr5Y65Ts+v1sSBExyZErUDZvLDvkmCLxQxdw04S6xwyb3sYTsf7fKBgTGcYoq1Lc/xOBSnoxuSMKBXXkDvfUvzAd8T12jj2txEDJifWDsQOK1fkqZdYJE1KpVaASstwhmif4kCPb3wFNsFt94K07/RxusSkM0a1NvXbDFyoXbtVzUwS+qzZ/aTDYjSvqGBzl7Unby5pBgvSdrsF3oUffSnRY8yXscjAOSH4FzSIrgAiOeRreprJlLKhOiRJyeQ="], stdout=PIPE).communicate()[0]

            service_code = '0900'
            broker_message_command = ["java","-Dfile.encoding=euc-kr","-cp","./libs/jars/billgateAPI.jar","com.galaxia.api.EncryptServiceBroker","./libs/config/config.ini",service_code]
            broker_message_command.append(message)

            return_message = Popen(broker_message_command, stdout=PIPE).communicate()[0]
            return_message = return_message.strip()

            return_code = return_message[0:5]

            this_data = {}

            if return_code=='ERROR':

                this_version = "0100"
                this_merchantId = service_id
                this_serviceCode = service_code
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

    payment_id=0

    if is_success:

        user_ = helper_get_user(request)

        payment = Payment.objects.create(
            user=user_,
            service_id=service_id,
            order_id=order_id,
            order_date=order_date,
            transaction_id=transaction_id[0],
            auth_amount=auth_amount[0],
            auth_date=auth_date[0],
            response_code=response_code,
            response_message=response_message[0],
            detail_response_code=detail_response_code[0],
            detail_response_message=detail_response_message[0]
        )
        if payment is not None:
            payment_id = payment.id

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



    # return render(request, 'return_explorer.html', {
    #     'response_code': response_code,
    #     'check_sum': check_sum,
    #     'is_success': is_success,
    #     'service_id': service_id,
    #     'order_id': order_id,
    #     'order_date': order_date,
    #
    # })

@csrf_exempt
def payment_return_explore_view(request):

    is_success = None
    service_id = None
    order_id = None
    order_date = None
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
        temp = service_id+order_id+order_date
        checksum_command = 'java -cp ./libs/jars/billgateAPI.jar com.galaxia.api.util.ChecksumUtil ' + \
        'DIFF ' + check_sum + " " + temp
        checksum = Popen(checksum_command.split(' '), stdout=PIPE).communicate()[0]
        checksum = checksum.strip()
        if checksum == 'SUC':


    # #         # function ServiceBroker('java -Dfile.encoding=euc-kr -cp ./libs/jars/billgateAPI.jar com.galaxia.api.EncryptServiceBroker',
    # #         #  './libs/config/config.ini')
    #         bin = 'java -Dfile.encoding=euc-kr -cp ./libs/jars/billgateAPI.jar com.galaxia.api.EncryptServiceBroker '
    #         config_file = '"/Users/ramju/Documents/workspace/django/project_motion9/motion9/libs/config/config.ini"'
    #         service_code = '"0900"'
    #         broker_message_command = bin+' '+config_file+' '+service_code+' "'+message + '"';
    #         print broker_message_command
    #         return_message = Popen(["java","-Dfile.encoding=euc-kr","-cp","./libs/jars/billgateAPI.jar","com.galaxia.api.EncryptServiceBroker","./libs/config/config.ini","0900","07180100      glx_api             0900y4w2jWCkhK6+7CTywaME87rUuYBO/yNgXErm0CgTv1GKQmU3eQvB+cGoFgo/w5R0hAiXS80Pcifm03Cen8rcbjR+46fB1uVPCFkB//Ois0jyJsSR9SN2Hr9C20EylIYSGc3uue86jc7G2L91ocZec7Y0JaiQZ6Qc6AdC/WxvPPueE0EzT4gx+mIAcCpMEBKdPtsCk+/Gcj2tXziqEM0HuumMgWtZI6ffhxQJNc/LuRpb6lM+JSPcO3eilE3XcQgtLWbkPeYduceVnRoaMG0fmec6Bhyy7HcjXiYTEG432G08KoaFPDXCUJp0anqlRjwzGo1w2h7+SFvTync32Bw1x195YR1I3biKGhvhS9iglgZ2Gb1TP8cZBdhZvCXqTMiUqEIRo2cKsqjHenfn4bAHvNrmOBeixCkcVHtnKtTEN26A4Cr5Y65Ts+v1sSBExyZErUDZvLDvkmCLxQxdw04S6xwyb3sYTsf7fKBgTGcYoq1Lc/xOBSnoxuSMKBXXkDvfUvzAd8T12jj2txEDJifWDsQOK1fkqZdYJE1KpVaASstwhmif4kCPb3wFNsFt94K07/RxusSkM0a1NvXbDFyoXbtVzUwS+qzZ/aTDYjSvqGBzl7Unby5pBgvSdrsF3oUffSnRY8yXscjAOSH4FzSIrgAiOeRreprJlLKhOiRJyeQ="], stdout=PIPE).communicate()[0]

            service_code = '0900'
            broker_message_command = ["java","-Dfile.encoding=euc-kr","-cp","./libs/jars/billgateAPI.jar","com.galaxia.api.EncryptServiceBroker","./libs/config/config.ini",service_code]
            broker_message_command.append(message)

            return_message = Popen(broker_message_command, stdout=PIPE).communicate()[0]
            return_message = return_message.strip()

            return_code = return_message[0:5]

            this_data = {}

            if return_code=='ERROR':

                this_version = "0100"
                this_merchantId = service_id
                this_serviceCode = service_code
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

    payment_id=0

    if is_success:

        user_ = helper_get_user(request)

        payment = Payment.objects.create(
            user=user_,
            service_id=service_id,
            order_id=order_id,
            order_date=order_date,
            transaction_id=transaction_id[0],
            auth_amount=auth_amount[0],
            auth_date=auth_date[0],
            response_code=response_code,
            response_message=response_message[0],
            detail_response_code=detail_response_code[0],
            detail_response_message=detail_response_message[0]
        )
        if payment is not None:
            payment_id = payment.id

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



    # return render(request, 'return_explorer.html', {
    #     'response_code': response_code,
    #     'check_sum': check_sum,
    #     'is_success': is_success,
    #     'service_id': service_id,
    #     'order_id': order_id,
    #     'order_date': order_date,
    #
    # })

@csrf_exempt
def payment_complete_view(request, payment_id=0):
    payment = Payment.objects.get(id=payment_id)
    return render(request, 'payment_complete_web.html', {
        'payment_amount': payment.auth_amount
    })

@csrf_exempt
def index_view(request):
    product_categories = Category.objects.filter(is_set=False).all()
    set_categories = Category.objects.filter(is_set=True).all()

    return render(request, 'index_web.html',
                  {
                      'product_categories': product_categories,
                      'set_categories': set_categories,
                      'next': 'index'
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

    return render(request, 'shopping_product_web.html',
                  {

                      'products': products_,
                      'current_category': current_category,
                      'current_category_id': category_id,
                      'categories': categories,
                      'current_page': 'shop_product',
                      'current_brand': brandname_filter,
                      'brands': brands
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

    return render(request, 'shopping_set_web.html',
                  {
                      'sets': sets,
                      'current_category': current_category,
                      'current_category_id': category_id,
                      'categories': categories,
                      'current_page': 'shop_set',
                      'brands': brands
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
        blog_reivews = helper_get_blog_reviews(product_id)
        # magazines

        return render(request, "product_detail_web.html",
                      {
                          'product': product,
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

    print custom_sets

    return render(request, "shopping_custom_web.html",
          {
              'custom_sets': custom_sets
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

    print data

    post_json = json.loads(data)
    set_id = post_json.get('set_id')
    custom_list = post_json.get('custom_lists')

    if set_id is None:
        return HttpResponse('is error')

    if user is not None:
        custom_set, is_created = CustomSet.objects.get_or_create(user=user, set_id=set_id)
        for custom_item in custom_list:
            original_id = custom_item.get('original_id')
            new_id = custom_item.get('new_id')
            if CustomSetDetail.objects.filter(custom_set=custom_set, original_product_id=original_id).exists():
                CustomSetDetail.objects.filter(custom_set=custom_set, original_product_id=original_id).update(new_product=new_id)
            else:
                CustomSetDetail.objects.create(custom_set=custom_set, original_product_id=original_id, new_product_id=new_id)
        return http_response_by_json()
    else:
        return http_response_by_json(CODE_LOGIN_REQUIRED)


# render example
# return render_to_response('shopping_product_web.html',
#               {
#                   'products': products_,
#                   'current_category': current_category,
#                   'categories': categories,
#                   'current_page': 'shop_product'
#               }, RequestContext(request))