# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.utils import DataError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from motion9 import const

from motion9.const import *
from common_controller.util import helper_get_user, helper_get_product_detail, helper_get_set, helper_make_paging_data, \
    helper_add_product_interest, helper_add_set_interest, helper_delete_product_interest, helper_delete_set_interest, \
    helper_add_product_cart, helper_add_set_cart, helper_add_custom_set_cart, \
    helper_delete_product_cart, helper_delete_set_cart, helper_delete_custom_set_cart, \
    helper_add_product_purchase, helper_add_set_purchase, helper_add_custom_set_purchase, \
    helper_delete_product_purchase, helper_delete_set_purchase, helper_delete_custom_set_purchase, \
    http_response_by_json, helper_make_custom_set, helper_get_custom_set, validateEmail, helper_get_cart_items, \
    helper_update_cart_items_count, helper_get_purchase_status, helper_get_user_ip, \
    helper_get_billgate_payment_checksum, helper_get_type_name

from .models import Interest

from subprocess import call, Popen, PIPE
import logging
import urllib2
import json
import time
from users.models import OrderTempInfo

logger = logging.getLogger(__name__)
# def helper_add_product_cart(user, product_id):
#     try:
#         Cart.objects.create(user=user, )

@csrf_exempt
def check_email_view(request):
    email = request.POST.get('email')

    if User.objects.filter(email=email).exists():
        return http_response_by_json(None, {'exist':True})

    return http_response_by_json(None, {'isValid': validateEmail(email), 'exist':False})

@csrf_exempt
def check_facebook_token_view(request, next='index'):
    token = request.POST.get('token', None)
    email = request.POST.get('email', None)

    if token is None:
        http_response_by_json( const.CODE_PARAMS_WRONG )
    else:

        app_token_url = 'https://graph.facebook.com/v2.0/oauth/access_token?client_id=1450591788523941&client_secret=f99304b17095fd8c2a7d737a9be8c39b&grant_type=client_credentials'
        contents = urllib2.urlopen(app_token_url).read()
        app_token = contents[13:]


        token_check_url = 'https://graph.facebook.com/debug_token?input_token='+token+'&access_token='+app_token

        contents = urllib2.urlopen(token_check_url).read()
        contents_dict = json.loads(contents)

        if contents_dict['data']['is_valid']==True:
            try:
                user_ = User.objects.get(username=email)
                user_.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user_)

                return redirect(next)

            except ObjectDoesNotExist as e:
                return redirect('registration_page')

        else:
            http_response_by_json( const.CODE_FACEBOOK_TOKEN_IS_NOT_VALID )


@csrf_exempt
def registration(request, next='index'):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    sex = request.POST.get('sex')

    if User.objects.filter(email=email).exists():
        return HttpResponse('already exist email')

    if password == password_confirm:
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.profile.name=name
            user.profile.sex=sex
            user.profile.save()
        except ValueError as e:
            logger.error(e)
            return HttpResponse('Registraion ValueError!')
        except IntegrityError as e:
            logger.error(e)
            return HttpResponse('Registraion IntegrityError!')

    else:
        return HttpResponse('password and confirm is not identical')

    user = authenticate(username=email, password=password)
    if user is not None and user.is_active:
        auth_login(request, user)

    return redirect(next)

@csrf_exempt
def registration_view(request):
    return render(request, 'register_web.html', {
        'next':'index'
    })

@csrf_exempt
def mobile_registration_view(request):
    return render(request, 'register.html')

@csrf_exempt
def login_(request, next='login_page'):
    email = request.POST.get('email')
    password = request.POST.get('password')

    error = None

    if not(User.objects.filter(email=email).exists()):
        error = '아이디가 존재하지 않습니다.'
        logger.error(error)
    else:
        user = authenticate(username=email, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect(next)
        else:
            error = '로그인에 실패하였습니다.'
            logger.error(error)

    messages.info(request, error)
    return redirect(next)

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated():
        return redirect('index')

    next = request.GET.get('next', 'login_page')
    return render(request, 'login_web.html',
        {
            'next': next
        })

@csrf_exempt
def logout_(request):
    next = request.GET.get('next', 'index')
    logout(request)
    return redirect( next )

@csrf_exempt
@login_required
def account_modify_view(request):
    user_ = helper_get_user(request)
    user_profile = user_.profile
    phone = user_profile.phone
    phones = phone.split("-")
    phone1 = phone2 = phone3 = ''
    if len(phones) == 3:
        phone1 = phones[0]
        phone2 = phones[1]
        phone3 = phones[2]

    return render(request, 'update_user_profile_web.html', {
        'user_profile': user_profile,
        'phone1': phone1,
        'phone2': phone2,
        'phone3': phone3,
    } )

@csrf_exempt
@login_required
def update(request):

    if helper_get_user(request) is not None:
        user_profile = request.user.profile

        name = request.POST.get('name', '')

        if len(name)>0:
            user_profile.name=name

        phone1=request.POST.get('phone1','')
        phone2=request.POST.get('phone2','')
        phone3=request.POST.get('phone3','')
        if len(phone1+phone2+phone3)>0:
            user_profile.phone = phone1+"-"+phone2+"-"+phone3
            
        recent_phone = request.POST.get('recent_phone', '')
        if len(recent_phone)>0:
            user_profile.recent_phone = recent_phone

        postcode = request.POST.get('postcode', '')
        if len(postcode)>0:
            user_profile.postcode = postcode
            
        basic_address = request.POST.get('basic_address', '')
        if len(basic_address)>0:
            user_profile.basic_address = basic_address
            
        detail_address = request.POST.get('detail_address', '')
        if len(detail_address)>0:
            user_profile.detail_address = detail_address
            
        sex = request.POST.get('sex', '')
        if len(sex)>0:
            user_profile.sex = sex
            
        age = request.POST.get('age', 0)
        if age>0:
            user_profile.age = age
            
        skin_type = request.POST.get('skin_type', '')
        if len(skin_type)>0:
            user_profile.skin_type = skin_type
            
        skin_color = request.POST.get('skin_color', '')
        if len(skin_color)>0:
            user_profile.skin_color = skin_color

        try:
            user_profile.save()
            return redirect('mypage')
        except DataError:
            logger.error('date input format not correct')
    else:
        logger.error('have_to_login')

@login_required
def mypage_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        interests = user.interest_set.filter(type='p').all()
        products = []
        for interest in interests:
            product = interest.product
            product_ = helper_get_product_detail(product, user)
            products.append(product_)

        if page_num is not None:
            products = helper_make_paging_data(len(products), products[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data':products}

        return render(request, 'mypage_interesting_web.html',
            {
                'interests': products,
                'tab_name': 'interesting_product'
            })

    else:
        logger.error('have_to_login')

@login_required
def mypage_set_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        interests = user.interest_set.filter(type='s').all()
        sets = []
        for interest in interests:
            set = interest.set
            set_ = helper_get_set(set, user)
            sets.append(set_)

        if page_num is not None:
            sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            sets = {'data':sets}

        return render(request, 'mypage_interesting_set_web.html',
            {
                'interests': sets,
                'tab_name': 'interesting_set'
            })

    else:
        logger.error('have_to_login')

@csrf_exempt
def billgate_payment_checksum(request):
    service_id=request.POST.get('service_id')
    order_id=request.POST.get('order_id')
    amount=request.POST.get('amount')

    checksum = helper_get_billgate_payment_checksum(service_id+order_id+amount)

    return http_response_by_json(None, {'checksum':checksum})


@login_required
def mypage_cart_view(request):

    current_datetime = time.strftime("%Y%m%d%H%M%S")
    user_ = helper_get_user(request)
    order_id = current_datetime+'_'+str(user_.id)
    cart_items = helper_get_cart_items( user_, order_id )
    OrderTempInfo.objects.create(order_id=order_id, original_amount=str(cart_items['total_price']))

    service_id = 'M1406684' # TEST:'glx_api', REAL:'M1406684'
    order_date = current_datetime
    item_code = str(user_.id)+"_"+current_datetime[8:]
    amount = str(cart_items['total_price'])
    user_ip = helper_get_user_ip(request)
    return_url = request.build_absolute_uri(reverse('payment_return'))
    using_type = '0000'
    currency = '0000'
    installment_period = '0'

    # checksum
    checksum = helper_get_billgate_payment_checksum(service_id+order_id+amount)

    if checksum=='8001' or checksum=='8003' or checksum=='8009':
        return HttpResponse('error code : '+checksum+' \nError Message: make checksum error! Please contact your system administrator!')

    payment_items = {
        'service_id': service_id,
        'order_id': order_id,
        'order_date': order_date,
        'user_id': user_.username,
        'item_code': item_code,
        'using_type': using_type,
        'currency': currency,
        'item_name': '',
        'amount': amount,
        'user_ip': user_ip,
        'installment_period': installment_period,
        'return_url': return_url,
        'check_sum': checksum
    }

    user_profile = user_.profile
    phone = user_profile.phone
    phones = phone.split("-")
    phone1 = phone2 = phone3 = ''
    if len(phones)==3:
        phone1=phones[0]
        phone2=phones[1]
        phone3=phones[2]

    profile_items = {
        'phone1': phone1,
        'phone2': phone2,
        'phone3': phone3,
    }

    if cart_items is not None:
        cart_items.update( {
            'payment_items': payment_items,
            'profile_items': profile_items,
            'user_profile': user_profile
        } )
        return render(request, 'cart_web.html', cart_items )
    else:
        return redirect('login_page')


@csrf_exempt
def mypage_cart_json_view(request):
    cart_items = helper_get_cart_items( helper_get_user(request) )

    if cart_items is not None:
        return http_response_by_json(None, cart_items)
    else:
        return http_response_by_json(None, {})

@csrf_exempt
@login_required
def mypage_purchase_view(request, page_num=1):
    page_num = int(page_num)
    purchases = request.user.purchase_set.all()
    purchase_list = []
    for purchase in purchases:
        if purchase.type=='p':
            product_ = helper_get_product_detail(purchase.product, request.user)
            purchase_list.append(product_)
        elif purchase.type=='s':
            set_ = helper_get_set(purchase.set, request.user)
            purchase_list.append(set_)
        elif purchase.type=='c':
            custom_set_ = helper_get_custom_set(purchase.custom_set, request.user)
            purchase_list.append(custom_set_)

        item = purchase_list.pop()
        item['total_price'] = purchase.price * purchase.item_count
        item['purchase'] = purchase
        item['payment'] = purchase.payment
        item['type_name'] = helper_get_type_name(purchase.type)
        item['status_name'] = helper_get_purchase_status(purchase.payment.status)
        purchase_list.append(item)

    purchase_list = helper_make_paging_data(len(purchase_list), purchase_list[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)

    # return render(request, 'mypage_interesting_set_web.html',
    return render(request, 'mypage_purchase_list_web.html',
                  {
                      'purchases': purchase_list,
                      'tab_name': 'purchase_list'
                  })
    # page_num = int(page_num)
    # user = helper_get_user(request)
    # if user is not None:
    #     purchases = user.purchase_set.all()
    #     purchases_ = []
    #     for purchase in purchases:
    #         if purchase.type=='p':
    #             product = purchase.product
    #             product_ = helper_get_product_detail(product, user)
    #             purchases_.append(product_)
    #         elif purchase.type=='s':
    #             set = purchase.set
    #             set_ = helper_get_set(set, user)
    #             purchases_.append(set_)
    #         elif purchase.type=='c':
    #             custom_set = purchase.custom_set
    #             custom_set_ = helper_get_custom_set(custom_set, user)
    #             purchases_.append(custom_set_)
    #
    #     if page_num is not None:
    #         purchases_ = helper_make_paging_data(len(purchases_), purchases_[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
    #     else:
    #         purchases_ = {'data':purchases_}
    #
    #     return render(request, 'my_page_purchase.html',
    #         {
    #             'purchases': purchases_,
    #             'tab_name':'purchase'
    #         })

@csrf_exempt
@login_required
def mypage_purchase_product_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        purchases = user.purchase_set.filter(type='p').all()
        products = []
        for purchase in purchases:
            payment = purchase.payment
            product = purchase.product
            product_ = helper_get_product_detail(product, user)
            product_.update({
                'item_count':purchase.item_count,
                'status':helper_get_purchase_status(payment.status),
                'shipping_number':payment.shipping_number,
                'price':purchase.price,
                'created':purchase.created
            })
            products.append(product_)

        if page_num is not None:
            products = helper_make_paging_data(len(products), products[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data':products}

        # return HttpResponse(json.dumps(products, ensure_ascii=False), content_type="application/json; charset=utf-8")

        return render(request, 'mypage_purchase_product_web.html',
            {
                'purchases': products,
                'tab_name': 'purchase_product'
            })

@login_required
def mypage_purchase_set_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        purchases = user.purchase_set.filter(type='s').all()
        sets = []
        for purchase in purchases:
            payment = purchase.payment
            set = purchase.set
            set_ = helper_get_set(set, user)
            set_.update({
                'item_count':purchase.item_count,
                'status':helper_get_purchase_status(payment.status),
                'shipping_number':payment.shipping_number,
                'price':purchase.price,
                'created':purchase.created
            })
            sets.append(set_)

        if page_num is not None:
            sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            sets = {'data':sets}

        return render(request, 'mypage_purchase_set_web.html',
            {
                'purchases': sets,
                'tab_name': 'purchase_product'
            })

@login_required
def mypage_purchase_custom_set_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        purchases = user.purchase_set.filter(type='c').all()
        custom_sets = []
        for purchase in purchases:
            payment = purchase.payment
            custom_set = purchase.custom_set
            custom_set_ = helper_get_custom_set(custom_set, user)
            custom_set_.update({
                'item_count':purchase.item_count,
                'status':helper_get_purchase_status(payment.status),
                'shipping_number':payment.shipping_number,
                'price':purchase.price,
                'created':purchase.created
            })
            custom_sets.append(custom_set_)

        if page_num is not None:
            custom_sets = helper_make_paging_data(len(custom_sets), custom_sets[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            custom_sets = {'data':custom_sets}

        return render(request, 'mypage_purchase_custom_web.html',
            {
                'purchases': custom_sets,
                'tab_name': 'purchase_product'
            })

@csrf_exempt
def add_interest(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_add_product_interest(user, product_or_set_id)
    elif type=='s':
        helper_add_set_interest(user, product_or_set_id)

    return http_response_by_json()

@csrf_exempt
def delete_interest(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_delete_product_interest(user, product_or_set_id)
    elif type=='s':
        helper_delete_set_interest(user, product_or_set_id)

    return http_response_by_json()


@csrf_exempt
def add_cart(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')
    item_count = int(request.POST.get('how_many', 1))

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_add_product_cart(user, product_or_set_id, item_count)
    elif type=='s':
        helper_add_set_cart(user, product_or_set_id, item_count)
    elif type=='c':
        helper_add_custom_set_cart(user, product_or_set_id, item_count)

    return http_response_by_json()

@csrf_exempt
def delete_cart(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')
    product_or_set_id = request.POST.get('product_or_set_id')

    if type=='p':
        helper_delete_product_cart(user, product_or_set_id)
    elif type=='s':
        helper_delete_set_cart(user, product_or_set_id)
    elif type=='c':
        helper_delete_custom_set_cart(user, product_or_set_id)

    return http_response_by_json()

@csrf_exempt
def add_purchase(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    address = request.POST.get('address', '')

    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_add_product_purchase(user, address, product_or_set_id)
    elif type=='s':
        helper_add_set_purchase(user, address, product_or_set_id)
    elif type=='c':
        helper_add_custom_set_purchase(user, address, product_or_set_id)

    return http_response_by_json()

@csrf_exempt
def delete_purchase(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    address = request.POST.get('address', '')

    type = request.POST.get('type', 'p')
    # delete need address ?

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_delete_product_purchase(user, address, product_or_set_id)
    elif type=='s':
        helper_delete_set_purchase(user, address, product_or_set_id)
    elif type=='c':
        helper_delete_custom_set_purchase(user, address, product_or_set_id)

    return http_response_by_json()

# make custom

@csrf_exempt
def make_custom_set(request):
    set_id = request.POST.get('set_id', -1)
    original_product_id = request.POST.get('original_product_id', -1)
    new_product_id = request.POST.get('new_product_id', -1)

    if set_id==-1 or original_product_id==-1 or new_product_id==-1:
        return http_response_by_json(CODE_PARAMS_WRONG)

    helper_make_custom_set( helper_get_user(request), set_id, original_product_id, new_product_id)
    return http_response_by_json(None)

# mobile part

def mobile_login_view(request):
    return render(request, 'login.html', {
        'next': 'mobile_index'
    })

def mobile_mypage_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        interests = user.interest_set.filter(type='p').all()
        products = []
        for interest in interests:
            product = interest.product
            product_ = helper_get_product_detail(product, user)
            products.append(product_)

        if page_num is not None:
            products = helper_make_paging_data(len(products), products[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data':products}

        return render(request, 'my_page_interesting.html',
            {
                'interests': products,
                'tab_name': 'interesting_product'
            })

    else:
        logger.error('have_to_login')

def mobile_mypage_set_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        interests = user.interest_set.filter(type='s').all()
        sets = []
        for interest in interests:
            set = interest.set
            set_ = helper_get_set(set, user)
            sets.append(set_)

        if page_num is not None:
            sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            sets = {'data':sets}

        return render(request, 'my_page_interesting_set.html',
            {
                'interests': sets,
                'tab_name': 'interesting_set'
            })

    else:
        logger.error('have_to_login')

def mobile_mypage_cart_view(request):

    cart_items = helper_get_cart_items( helper_get_user(request) )
    return render(request, 'cart.html', cart_items)


@csrf_exempt
def mobile_mypage_before_purchase_view(request):
    product_id_list = request.POST.get('product_id', None)
    product_count_list = request.POST.get('product_cnt', None)

    if product_id_list is not None and product_count_list is not None\
            and len(product_id_list) == len(product_count_list):
        helper_update_cart_items_count( helper_get_user(request),
                                        product_id_list,
                                        product_count_list,
                                        'p')

    set_id_list = request.POST.get('set_id', None)
    set_count_list = request.POST.get('set_cnt', None)

    if set_id_list is not None and set_count_list is not None\
            and len(set_id_list) == len(set_count_list):
        helper_update_cart_items_count( helper_get_user(request),
                                        set_id_list,
                                        set_count_list,
                                        's')

    custom_set_id_list = request.POST.get('custom_set_id', None)
    custom_set_count_list = request.POST.get('custom_set_cnt', None)

    if custom_set_id_list is not None and custom_set_count_list is not None\
            and len(custom_set_id_list) == len(custom_set_count_list):
        helper_update_cart_items_count( helper_get_user(request),
                                        custom_set_id_list,
                                        custom_set_count_list,
                                        'c')

    cart_items = helper_get_cart_items( helper_get_user(request) )

    current_datetime = time.strftime("%Y%m%d%H%M%S")
    order_id = 'motion9_' + current_datetime
    user_ = helper_get_user(request)

    cart_items = helper_get_cart_items( user_, order_id )

    # testing option
    # service_id = 'glx_api'
    service_id = 'M1406684'
    order_date = current_datetime
    item_name = user_.username+"_"+current_datetime
    item_code = str(user_.id)+"_"+current_datetime[8:]
    amount = str(cart_items['total_price'])
    installment_period='0:3'
    return_url = request.build_absolute_uri(reverse('payment_return_mobile_web'))

    payment_items = {
        'service_id': service_id,
        'order_id': order_id,
        'order_date': order_date,
        'user_id': user_.username,
        'user_name': user_.profile.name,
        'user_email': user_.email,
        'item_code': item_code,
        'item_name': item_name,
        'card_type': '',
        'amount': amount,
        'installment_period': installment_period,
        'return_url': return_url,
        'appname': 'WEB'
    }

    if cart_items is not None:
        cart_items.update( {'payment_items':payment_items} )
        return render(request, 'purchase.html', cart_items )
    else:
        return redirect('mobile_login_page')

