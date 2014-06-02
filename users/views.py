from django.db import IntegrityError
from django.db.utils import DataError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from common_controller.util import helper_get_user, helper_get_product

from .models import Interest

import logging

logger = logging.getLogger(__name__)

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
        interests = user.interest_set.all()
        products = []
        for interest in interests:
            product = interest.product
            product_ = helper_get_product(product.id, user)
            products.append(product_)

        return render(request, 'mypage_interesting_web.html',
            {
                'interests': products,
                'tab_name': 'interesting_set'
            })

    else:
        logger.error('have_to_login')

# return render(request, 'shopping_product_web.html',
#                   {
#
#                       'products': products_,
#                       'current_category': current_category,
#                       'categories': categories,
#                       'current_page': 'shop_product'
#                   })