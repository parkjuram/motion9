from django.db import IntegrityError
from django.db.utils import DataError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from motion9.const import *
from common_controller.util import helper_get_user, helper_get_product, helper_get_set, helper_make_paging_data

from .models import Interest

import logging

logger = logging.getLogger(__name__)

def helper_add_product_interest(user, product_id):
    try:
        Interest.objects.create(user=user, product_id=product_id, type='p')
    except Exception as e:
        logger.error(e)

def helper_delete_product_interest(user, product_id):
    try:
        interest = Interest.objects.get(user=user, product_id=product_id, type='p')
        interest.delete()
    except Exception as e:
        logger.error(e)

def helper_add_set_interest(user, set_id):
    try:
        Interest.objects.create(user=user, set_id=set_id, type='s')
    except Exception as e:
        logger.error(e)

def helper_delete_set_interest(user, set_id):
    try:
        interest = Interest.objects.get(user=user, set_id=set_id, type='s')
        interest.delete()
    except Exception as e:
        logger.error(e)

@csrf_exempt
def registration(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')

    if password == password_confirm:
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except ValueError as e:
            logger.error(e)
        except IntegrityError as e:
            logger.error(e)

    else:
        logger.error('password and confirm is not identical')

    return HttpResponse('temporary response')

@csrf_exempt
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not(User.objects.filter(username=email).exists()):
        logger.error('user id is not exsit')
    else:
        user = authenticate(username=email, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect('shop_product')
        else:
            logger.error('login fail')

@csrf_exempt
def login_view(request):
    return render(request, 'login_web.html')

@login_required
def logout(request):
    logout(request)

@login_required
def update(request):

    if helper_get_user(request) is not None:
        user_profile = request.user.profile

        user_profile.name = request.POST.get('name')
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
def mypage_view(request, page_num=None):
    user = helper_get_user(request)
    if user is not None:
        interests = user.interest_set.filter(type='p').all()
        products = []
        for interest in interests:
            product = interest.product
            product_ = helper_get_product(product, user)
            products.append(product_)

        if page_num is not None:
            products = helper_make_paging_data(len(products), products[(page_num-1)*ITEM_COUNT_PER_PAGE:page_num*ITEM_COUNT_PER_PAGE], page_num)
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
def mypage_set_view(request, page_num=None):
    user = helper_get_user(request)
    if user is not None:
        interests = user.interest_set.filter(type='s').all()
        sets = []
        for interest in interests:
            set = interest.set
            set_ = helper_get_set(set, user)
            sets.append(set_)

        if page_num is not None:
            sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE:page_num*ITEM_COUNT_PER_PAGE], page_num)
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
def mypage_purchase_view(request, page_num=None):
    pass

@login_required
def mypage_cart_view(request):
    # user = helper_get_user(request)
    # products = user.cart_set.filter(type='p').all()
    pass

@csrf_exempt
@login_required
def add_interest(request):
    user = helper_get_user(request)
    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_add_product_interest(user, product_or_set_id)
    elif type=='s':
        helper_add_set_interest(user, product_or_set_id)

    return HttpResponse('temporary response')

@login_required
def delete_interest(request):
    user = helper_get_user(request)
    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type=='p':
        helper_delete_product_interest(user, product_or_set_id)
    elif type=='s':
        helper_delete_set_interest(user, product_or_set_id)

    return HttpResponse('temporary response')

# return render(request, 'shopping_product_web.html',
#                   {
#
#                       'products': products_,
#                       'current_category': current_category,
#                       'categories': categories,
#                       'current_page': 'shop_product'
#                   })