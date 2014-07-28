from django.db import IntegrityError
from django.db.utils import DataError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from motion9.const import *
from common_controller.util import helper_get_user, helper_get_product_detail, helper_get_set, helper_make_paging_data, \
    helper_add_product_interest, helper_add_set_interest, helper_delete_product_interest, helper_delete_set_interest, \
    helper_add_product_cart, helper_add_set_cart, helper_add_custom_set_cart, \
    helper_delete_product_cart, helper_delete_set_cart, helper_delete_custom_set_cart, \
    helper_add_product_purchase, helper_add_set_purchase, helper_add_custom_set_purchase, \
    helper_delete_product_purchase, helper_delete_set_purchase, helper_delete_custom_set_purchase, \
    http_response_by_json, helper_make_custom_set, helper_get_custom_set, validateEmail, helper_get_cart_items, \
    helper_update_cart_items_count

from .models import Interest

import logging

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
def registration(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')

    if User.objects.filter(email=email).exists():
        return HttpResponse('already exist email')

    if password == password_confirm:
        try:
            user = User.objects.create_user(username=name, email=email, password=password)
        except ValueError as e:
            logger.error(e)
            return HttpResponse('error')
        except IntegrityError as e:
            logger.error(e)
            return HttpResponse('error')

    else:
        return HttpResponse('password and confirm is not identical')

    return http_response_by_json(None)

@csrf_exempt
def registration_view(request):
    return render(request, 'register_web.html')

@csrf_exempt
def mobile_registration_view(request):
    return render(request, 'register.html')

@csrf_exempt
def login(request, next='index'):
    email = request.POST.get('email')
    password = request.POST.get('password')

    error = None

    if not(User.objects.filter(email=email).exists()):
        error = 'user id is not exsit'
        logger.error(error)
    else:
        user_ = User.objects.get(email=email)
        user = authenticate(username=user_.username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect(next)
        else:
            error = 'login fail'
            logger.error(error)

    return HttpResponse(error)

@csrf_exempt
def login_view(request):
    return render(request, 'login_web.html',
        {
            'next': 'shop_product'
        })

@csrf_exempt
def logout_(request):
    next = request.GET.get('next', 'index' )
    logout(request)
    return redirect( next )

@login_required
def update(request):

    if helper_get_user(request) is not None:
        user_profile = request.user.profile

        user_profile.phone = request.POST.get('phone')
        user_profile.address = request.POST.get('address')
        user_profile.sex = request.POST.get('sex')
        user_profile.age = request.POST.get('age')
        user_profile.skin_type = request.POST.get('skin_type')
        user_profile.skin_color = request.POST.get('skin_color')

        try:
            user_profile.save()
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

@login_required
def mypage_cart_view(request):
    cart_items = helper_get_cart_items( helper_get_user(request) )

    if cart_items is not None:
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

def mypage_purchase_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        purchases = user.purchase_set.all()
        purchases_ = []
        for purchase in purchases:
            if purchase.type=='p':
                product = purchase.product
                product_ = helper_get_product_detail(product, user)
                purchases_.append(product_)
            elif purchase.type=='s':
                set = purchase.set
                set_ = helper_get_set(set, user)
                purchases_.append(set_)
            elif purchase.type=='c':
                custom_set = purchase.custom_set
                custom_set_ = helper_get_custom_set(custom_set, user)
                purchases_.append(custom_set_)

        if page_num is not None:
            purchases_ = helper_make_paging_data(len(purchases_), purchases_[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            purchases_ = {'data':purchases_}

        return render(request, 'my_page_purchase.html',
            {
                'purchases': purchases_,
                'tab_name':'purchase'
            })

@login_required
def mypage_purchase_product_view(request, page_num=1):
    page_num = int(page_num)
    user = helper_get_user(request)
    if user is not None:
        purchases = user.purchase_set.filter(type='p').all()
        products = []
        for purchase in purchases:
            product = purchase.product
            product_ = helper_get_product_detail(product, user)
            products.append(product_)

        if page_num is not None:
            products = helper_make_paging_data(len(products), products[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data':products}

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
            set = purchase.set
            set_ = helper_get_product_detail(set, user)
            sets.append(set_)

        if page_num is not None:
            products = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data':sets}

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
            custom_set = purchase.custom_set
            custom_set_ = helper_get_product_detail(custom_set, user)
            custom_sets.append(custom_set_)

        if page_num is not None:
            products = helper_make_paging_data(len(custom_sets), custom_sets[(page_num-1)*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num*ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET], ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            products = {'data':custom_sets}

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

    return render(request, 'purchase.html', cart_items )