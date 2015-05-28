# -*- coding: utf-8 -*-
import hashlib
import random
from allauth.account import app_settings
from allauth.account.forms import SignupForm
from allauth.account.utils import get_next_redirect_url
from allauth.account.utils import complete_signup
from allauth.account.utils import passthrough_next_redirect_url
from allauth.account.views import RedirectAuthenticatedUserMixin, CloseableSignupMixin, AjaxCapableProcessFormViewMixin, \
    sensitive_post_parameters_m
from allauth.utils import get_form_class
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.utils import DataError
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from common.models import NCategory
from common_controller.decorators import mobile_login_required
from motion9 import const
from foradmin.models import MainImage, Advertisement, Preference
from motion9 import settings
from django.utils import timezone

from motion9.const import *
from common_controller.util import helper_get_user, helper_get_product_detail, helper_get_set, helper_make_paging_data, \
    helper_add_product_interest, helper_add_set_interest, helper_delete_product_interest, helper_delete_set_interest, \
    helper_add_product_cart, helper_add_set_cart, helper_add_custom_set_cart, \
    helper_delete_product_cart, helper_delete_set_cart, helper_delete_custom_set_cart, \
    helper_add_product_purchase, helper_add_set_purchase, helper_add_custom_set_purchase, \
    helper_delete_product_purchase, helper_delete_set_purchase, helper_delete_custom_set_purchase, \
    http_response_by_json, helper_make_custom_set, helper_get_custom_set, validateEmail, helper_get_cart_items, \
    helper_update_cart_items_count, helper_get_purchase_status, helper_get_user_ip, \
    helper_get_billgate_payment_checksum, helper_get_type_name, helper_get_payment_item, helper_get_profile_item, \
    helper_put_order_id_in_cart, helper_get_purchase_items, helper_get_products, helper_get_blog_reviews, \
    helper_get_product_magazines, helper_get_survey_items, \
    helper_request_survey

from .models import Interest, UserSurvey, UserSurveyMore, UserProfile

from subprocess import call, Popen, PIPE
import logging
import urllib2
import json
import time
from users.admin import UserSurveyAdmin
from users.models import OrderTempInfo, Cart, NInterest, UserSurveyAgain, UserSurveyDetail
from users import mp

logger = logging.getLogger(__name__)
# def helper_add_product_cart(user, product_id):
# try:
#         Cart.objects.create(user=user, )


# 이미 가입된 mail인지 확인하는 api
@csrf_exempt
def check_email_view(request):
    email = request.POST.get('email')

    if User.objects.filter(email=email).exists():
        return http_response_by_json(None, {'exist': True})

    return http_response_by_json(None, {'isValid': validateEmail(email), 'exist': False})


# facebook token이 유효한지 확인하는 api
@csrf_exempt
def check_facebook_token_view(request):
    next = request.GET.get('next', 'mobile:mobile_index' if request.is_mobile else 'index')
    token = request.POST.get('token', None)
    email = request.POST.get('email', None)

    if token is None:
        http_response_by_json(const.CODE_PARAMS_WRONG)
    else:
        app_token_url = 'https://graph.facebook.com/v2.0/oauth/access_token?client_id=1450591788523941&client_secret=f99304b17095fd8c2a7d737a9be8c39b&grant_type=client_credentials'
        contents = urllib2.urlopen(app_token_url).read()
        app_token = contents[13:]

        token_check_url = 'https://graph.facebook.com/debug_token?input_token=' + token + '&access_token=' + app_token

        contents = urllib2.urlopen(token_check_url).read()
        contents_dict = json.loads(contents)

        if contents_dict['data']['is_valid'] == True:
            try:
                user_ = User.objects.get(username=email)
                user_.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user_)

                return redirect(next)

            except ObjectDoesNotExist as e:
                if request.is_mobile:
                    return redirect('mobile_registration_page')
                else:
                    return redirect('registration_page')

        else:
            http_response_by_json(const.CODE_FACEBOOK_TOKEN_IS_NOT_VALID)


# 회원가입 api
@csrf_exempt
def registration(request, next='index'):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    sex = request.POST.get('sex')
    age = request.POST.get('age')

    error = None
    if User.objects.filter(email=email).exists():
        error = '이미 가입된 E-mail 입니다.'
    elif email == '':
        error = 'E-mail을 입력해 주세요.'
    elif password == '':
        error = '비밀번호를 입력해 주세요.'
    elif password != password_confirm:
        error = '비밀번호를 확인해 주세요.'
    elif name == '':
        error = '이름을 입력해 주세요.'

    if error is None:
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            # user.is_active = False
            # user.save()
            user.profile.name = name
            user.profile.sex = sex
            user.profile.age = age
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            user.profile.activation_key = hashlib.sha1(salt + email).hexdigest()
            user.profile.key_expires = datetime.datetime.today() + datetime.timedelta(2)
            user.profile.save()
        except ValueError as e:
            logger.error(e)
            error = 'Registraion ValueError!'
        except IntegrityError as e:
            logger.error(e)
            error = 'Registraion IntegrityError!'

    if error is None:
        # Send email with activation key
        # user=User.objects.get(username=email)

        # email_subject = 'Account confirmation'
        # email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
        # 48hours http://local.finers.co.kr:8000/users/confirm/%s" % (user.username, user.profile.activation_key)
        # send_mail(email_subject, email_body, 'test@finers.com', [user.email], fail_silently=False)
        # user = authenticate(username=email, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)

        return redirect(next)
    else:
        messages.info(request, error)
        return redirect(next)


# 회원가입 페이지
@csrf_exempt
def registration_view(request):
    next = request.GET.get('next', 'mobile_registration_page' if request.is_mobile else 'registration_page')
    if request.user.is_authenticated():
        return redirect('mobile:mobile_index' if request.is_mobile else 'index')

    return render(request, 'register_web.html', {
        'next': next
    })


# 모바일용 회원가입 페이지
@csrf_exempt
def mobile_registration_view(request):
    if request.user.is_authenticated():
        return redirect('mobile:mobile_index')

    next = request.GET.get('next', 'mobile_registration_page')

    return render(request, 'register.html', {
        'next': next
    })


# 로그인 api
@csrf_exempt
def login_(request, next='login_page'):
    email = request.POST.get('email')
    password = request.POST.get('password')

    error = None

    if not (User.objects.filter(email=email).exists()):
        error = '아이디가 존재하지 않습니다.'
        logger.error(error)
    else:
        user = authenticate(username=email, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            request.session['is_first_login'] = True

            return redirect(next)
        else:
            error = '로그인에 실패하였습니다.'
            logger.error(error)

    messages.info(request, error)
    return redirect(next)


# 로그인 페이지
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated():
        return redirect('index')

    next = request.GET.get('next', 'login_page')
    fail = request.GET.get('fail', 'registration_page')

    return render(request, 'login_web.html',
                  {
                      'next': next,
                      'fail': fail
                  })


# 로그아웃 api
@csrf_exempt
def logout_(request):
    next = request.GET.get('next', 'index')
    logout(request)
    return redirect(next)


# 계정정보 update 페이짘
@csrf_exempt
@login_required
def account_modify_view(request):
    next = request.GET.get('next', 'mypage')
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
        'next': next
    })


# user정보 update 페이지, 위의 view와 왜 중복되는지는 모르겠음
@csrf_exempt
@login_required
def update(request, next='mypage'):
    if helper_get_user(request) is not None:
        user_profile = request.user.profile

        name = request.POST.get('name', '')

        if len(name) > 0:
            user_profile.name = name

        phone1 = request.POST.get('phone1', '')
        phone2 = request.POST.get('phone2', '')
        phone3 = request.POST.get('phone3', '')
        if len(phone1 + phone2 + phone3) > 0:
            user_profile.phone = phone1 + "-" + phone2 + "-" + phone3

        recent_phone = request.POST.get('recent_phone', '')
        if len(recent_phone) > 0:
            user_profile.recent_phone = recent_phone

        postcode = request.POST.get('postcode', '')
        if len(postcode) > 0:
            user_profile.postcode = postcode

        basic_address = request.POST.get('basic_address', '')
        if len(basic_address) > 0:
            user_profile.basic_address = basic_address

        detail_address = request.POST.get('detail_address', '')
        if len(detail_address) > 0:
            user_profile.detail_address = detail_address

        sex = request.POST.get('sex', '')
        if len(sex) > 0:
            user_profile.sex = sex

        age = request.POST.get('age', 0)
        if age > 0:
            user_profile.age = age

        skin_type = request.POST.get('skin_type', '')
        if len(skin_type) > 0:
            user_profile.skin_type = skin_type

        skin_color = request.POST.get('skin_color', '')
        if len(skin_color) > 0:
            user_profile.skin_color = skin_color

        try:
            user_profile.save()
            return redirect(next)
            # return redirect('mypage')
        except DataError:
            logger.error('date input format not correct')
    else:
        logger.error('have_to_login')


# mypage 페이지
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
            products = helper_make_paging_data(len(products), products[(
                                                                       page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT],
                                               ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data': products}

        if user.profile.age is not None:
            user.profile.age = datetime.datetime.now().year - user.profile.age + 1
        else:
            user.profile.age = ''

        request.user.interest = request.user.ninterest_set.select_related('product').all()

        return render(request, 'mypage_interesting_web.html',
                      {
                          'interests': products,
                          'tab_name': 'interesting_product',
                          'categories': NCategory.objects.values()
                      })

    else:
        logger.error('have_to_login')


# mypage의 set 페이지
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
            sets = helper_make_paging_data(len(sets), sets[(
                                                           page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET],
                                           ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            sets = {'data': sets}

        return render(request, 'mypage_interesting_set_web.html',
                      {
                          'interests': sets,
                          'tab_name': 'interesting_set'
                      })

    else:
        logger.error('have_to_login')


# billgate 결제모듈 연동시 security를 위해 checksum을 구하는 api
@csrf_exempt
def billgate_payment_checksum(request):
    service_id = request.POST.get('service_id')
    order_id = request.POST.get('order_id')
    amount = request.POST.get('amount')

    checksum = helper_get_billgate_payment_checksum(service_id + order_id + amount)

    return http_response_by_json(None, {'checksum': checksum})


# mypage 카트 페이지
#@mobile_login_required
@login_required
def mypage_cart_view(request):
    cart_items = helper_get_cart_items(helper_get_user(request))
    payment_items = helper_get_payment_item(request, cart_items['total_price'])
    helper_put_order_id_in_cart(request.user, payment_items['order_id'])
    profile_items = helper_get_profile_item(request)

    if request.user.is_authenticated():
        cart_items.update({
            'payment_items': payment_items,
            'profile_items': profile_items,
            'user_profile': request.user.profile
        })
        return render(request, 'cart_web.html', cart_items)
    else:
        return redirect('login_page')


# mypage cart정보를 json 으로 뿌려주는 api
@csrf_exempt
def mypage_cart_json_view(request):
    cart_items = helper_get_cart_items(helper_get_user(request))

    if cart_items is not None:
        return http_response_by_json(None, cart_items)
    else:
        return http_response_by_json(None, {})


# mypage 구매 내역 페이지
@csrf_exempt
@login_required
def mypage_purchase_view(request, page_num=1):
    page_num = int(page_num)
    purchases = request.user.purchase_set.all()
    purchase_list = []
    for purchase in purchases:
        if purchase.type == 'p':
            product_ = helper_get_product_detail(purchase.product, request.user)
            purchase_list.append(product_)
        elif purchase.type == 's':
            set_ = helper_get_set(purchase.set, request.user)
            purchase_list.append(set_)
        elif purchase.type == 'c':
            custom_set_ = helper_get_custom_set(purchase.custom_set, request.user)
            purchase_list.append(custom_set_)

        item = purchase_list.pop()
        item['total_price'] = purchase.price * purchase.item_count
        item['purchase'] = purchase
        item['payment'] = purchase.payment
        item['type_name'] = helper_get_type_name(purchase.type)
        item['status_name'] = helper_get_purchase_status(purchase.payment.status)
        item['datetime'] = item['payment'].auth_date[:4] + "/" + item['payment'].auth_date[4:6] + "/" + item[
                                                                                                            'payment'].auth_date[
                                                                                                        6:8] + "\n" + \
                           item['payment'].auth_date[8:10] + ":" + item['payment'].auth_date[10:12]
        purchase_list.append(item)

    purchase_list = helper_make_paging_data(len(purchase_list), purchase_list[(
                                                                              page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT],
                                            ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)

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


# mypage 구매 내역 페이지에서 product 내역 페이지
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
                'item_count': purchase.item_count,
                'status': helper_get_purchase_status(payment.status),
                'shipping_number': payment.shipping_number,
                'price': purchase.price,
                'created': purchase.created
            })
            products.append(product_)

        if page_num is not None:
            products = helper_make_paging_data(len(products), products[(
                                                                       page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT],
                                               ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data': products}

        # return HttpResponse(json.dumps(products, ensure_ascii=False), content_type="application/json; charset=utf-8")

        return render(request, 'mypage_purchase_product_web.html',
                      {
                          'purchases': products,
                          'tab_name': 'purchase_product'
                      })


# mypage 구매 내역 페이지에서 set 내역 페이지
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
                'item_count': purchase.item_count,
                'status': helper_get_purchase_status(payment.status),
                'shipping_number': payment.shipping_number,
                'price': purchase.price,
                'created': purchase.created
            })
            sets.append(set_)

        if page_num is not None:
            sets = helper_make_paging_data(len(sets), sets[(
                                                           page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT],
                                           ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            sets = {'data': sets}

        return render(request, 'mypage_purchase_set_web.html',
                      {
                          'purchases': sets,
                          'tab_name': 'purchase_product'
                      })


# mypage 구매 내역 페이지에서 custom_set 내역 페이지
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
                'item_count': purchase.item_count,
                'status': helper_get_purchase_status(payment.status),
                'shipping_number': payment.shipping_number,
                'price': purchase.price,
                'created': purchase.created
            })
            custom_sets.append(custom_set_)

        if page_num is not None:
            custom_sets = helper_make_paging_data(len(custom_sets), custom_sets[(
                                                                                page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET],
                                                  ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            custom_sets = {'data': custom_sets}

        return render(request, 'mypage_purchase_custom_web.html',
                      {
                          'purchases': custom_sets,
                          'tab_name': 'purchase_product'
                      })


# 함수 명 그대로의 기능
@csrf_exempt
def add_interest(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type == 'p':
        helper_add_product_interest(user, product_or_set_id)
    elif type == 's':
        helper_add_set_interest(user, product_or_set_id)

    return http_response_by_json()


# 함수 명 그대로의 기능
@csrf_exempt
def delete_interest(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type == 'p':
        helper_delete_product_interest(user, product_or_set_id)
    elif type == 's':
        helper_delete_set_interest(user, product_or_set_id)

    return http_response_by_json()


# 함수 명 그대로의 기능
@csrf_exempt
def update_cart(request):
    cart_item_id = request.POST.get('cart_item_id', '')
    cart_item_count = request.POST.get('cart_item_count', '')

    if cart_item_id != '' and cart_item_count != '':
        try:
            cart_item = Cart.objects.get(id=cart_item_id)
            cart_item.item_count = cart_item_count
            cart_item.save()
        except ObjectDoesNotExist as e:
            return http_response_by_json(CODE_PARAMS_WRONG)

        cart_items = helper_get_cart_items(request.user)

        return http_response_by_json(None, {
            'total_price': cart_items['total_price']
        })
    return http_response_by_json(CODE_PARAMS_WRONG)


# 함수 명 그대로의 기능
@csrf_exempt
def add_cart(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')
    item_count = int(request.POST.get('how_many', 1))

    product_or_set_id = request.POST.get('product_or_set_id')
    if type == 'p':
        helper_add_product_cart(user, product_or_set_id, item_count)
    elif type == 's':
        helper_add_set_cart(user, product_or_set_id, item_count)
    elif type == 'c':
        helper_add_custom_set_cart(user, product_or_set_id, item_count)

    return http_response_by_json()


# 함수 명 그대로의 기능
@csrf_exempt
def delete_cart(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    type = request.POST.get('type', 'p')
    product_or_set_id = request.POST.get('product_or_set_id')

    if type == 'p':
        helper_delete_product_cart(user, product_or_set_id)
    elif type == 's':
        helper_delete_set_cart(user, product_or_set_id)
    elif type == 'c':
        helper_delete_custom_set_cart(user, product_or_set_id)

    return http_response_by_json()


# 함수 명 그대로의 기능
@csrf_exempt
def add_purchase(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    address = request.POST.get('address', '')

    type = request.POST.get('type', 'p')

    product_or_set_id = request.POST.get('product_or_set_id')
    if type == 'p':
        helper_add_product_purchase(user, address, product_or_set_id)
    elif type == 's':
        helper_add_set_purchase(user, address, product_or_set_id)
    elif type == 'c':
        helper_add_custom_set_purchase(user, address, product_or_set_id)

    return http_response_by_json()


# 함수 명 그대로의 기능
@csrf_exempt
def delete_purchase(request):
    user = helper_get_user(request)
    if user is None:
        return http_response_by_json(CODE_LOGIN_REQUIRED)

    address = request.POST.get('address', '')

    type = request.POST.get('type', 'p')
    # delete need address ?

    product_or_set_id = request.POST.get('product_or_set_id')
    if type == 'p':
        helper_delete_product_purchase(user, address, product_or_set_id)
    elif type == 's':
        helper_delete_set_purchase(user, address, product_or_set_id)
    elif type == 'c':
        helper_delete_custom_set_purchase(user, address, product_or_set_id)

    return http_response_by_json()


# make custom

# 함수 명 그대로의 기능
@csrf_exempt
def make_custom_set(request):
    set_id = request.POST.get('set_id', -1)
    original_product_id = request.POST.get('original_product_id', -1)
    new_product_id = request.POST.get('new_product_id', -1)

    if set_id == -1 or original_product_id == -1 or new_product_id == -1:
        return http_response_by_json(CODE_PARAMS_WRONG)

    helper_make_custom_set(helper_get_user(request), set_id, original_product_id, new_product_id)
    return http_response_by_json(None)


# mobile part

# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
def mobile_login_view(request):
    if request.user.is_authenticated():
        return redirect('mobile:mobile_index')

    next = request.GET.get('next', 'mobile_login_page')
    fail = request.GET.get('fail', 'mobile_registration_page')

    return render(request, 'login.html', {
        'next': next,
        'fail': fail
    })


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@login_required
def mobile_mypage_interesting_view(request, page_num=1):
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
            products = helper_make_paging_data(len(products), products[(
                                                                       page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT],
                                               ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_PRODUCT, page_num)
        else:
            products = {'data': products}

        return render(request, 'my_page_interesting.html',
                      {
                          'interests': products,
                          'tab_name': 'interesting_product'
                      })

    else:
        return redirect('mobile:mobile_index')


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@mobile_login_required
def mobile_mypage_myinfo_view(request, page_num=1):
    user = helper_get_user(request)
    if user is not None:

        if user.profile.age is not None:
            user.profile.age = datetime.datetime.now().year - user.profile.age + 1
        else:
            user.profile.age = ''

        request.user.interest = request.user.ninterest_set.select_related('product').all()
        categories = NCategory.objects.values()

        return render(request, 'my_page_myinfo.html',
                      {
                          'tab_name': 'myinfo',
                          'categories': categories
                      })

    else:
        logger.error('have_to_login')


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
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
            sets = helper_make_paging_data(len(sets), sets[(
                                                           page_num - 1) * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET:page_num * ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET],
                                           ITEM_COUNT_PER_PAGE_MYPAGE_INTEREST_SET, page_num)
        else:
            sets = {'data': sets}

        return render(request, 'my_page_interesting_set.html',
                      {
                          'interests': sets,
                          'tab_name': 'interesting_set'
                      })

    else:
        logger.error('have_to_login')


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
def mobile_mypage_cart_view(request):
    cart_items = helper_get_cart_items(helper_get_user(request))
    return render(request, 'cart.html', cart_items)


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@mobile_login_required
def mobile_mypage_purchase_list_view(request):
    purchase_items = helper_get_purchase_items(request)

    return render(request, 'mypage_purchase_list.html', {
        'purchase_items': purchase_items,
        'tab_name': 'purchase_list'
    })


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@csrf_exempt
@mobile_login_required
def mobile_mypage_before_purchase_view(request):
    cart_items = helper_get_cart_items(helper_get_user(request))
    payment_items = helper_get_payment_item(request, cart_items['total_price'], True)
    helper_put_order_id_in_cart(request.user, payment_items['order_id'])
    profile_items = helper_get_profile_item(request)

    cart_items.update({
        'payment_items': payment_items,
        'profile_items': profile_items,
        'user_profile': request.user.profile
    })

    return render(request, 'purchase.html', cart_items)


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@mobile_login_required
def mobile_mypage_myinfo_edit_view(request, page_num=1):
    user = helper_get_user(request)
    user_profile = user.profile

    next = request.GET.get('next', 'mobile_mypage')

    phone = user_profile.phone
    phones = phone.split("-")
    phone1 = phone2 = phone3 = ''
    if len(phones) == 3:
        phone1 = phones[0]
        phone2 = phones[1]
        phone3 = phones[2]

    if user is not None:

        return render(request, 'my_page_myinfo_edit.html',
                      {
                          'tab_name': 'myinfo',
                          'phone1': phone1,
                          'phone2': phone2,
                          'phone3': phone3,
                          'next': next
                      })

    else:
        logger.error('have_to_login')


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@mobile_login_required
def mobile_report_view(request, category_id=None, page_num=1):
    user = helper_get_user(request)
    user_profile = user.profile

    products_ = helper_get_products(helper_get_user(request), category_id)

    if page_num is not None:
        products_ = helper_make_paging_data(len(products_), products_[(
                                                                      page_num - 1) * ITEM_COUNT_PER_PAGE_FOR_PRODUCT:page_num * ITEM_COUNT_PER_PAGE_FOR_PRODUCT],
                                            ITEM_COUNT_PER_PAGE_FOR_PRODUCT, page_num)
    else:
        products_ = {'data': products_}

    if user is not None:

        return render(request, 'report.html',
                      {
                          'products': products_,
                          'tab_name': 'myinfo',
                          'next': next
                      })

    else:
        logger.error('have_to_login')


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@mobile_login_required
def mobile_report_detail_view(request, category_id=None, page_num=1, product_id=None):
    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))

        product['category_guide_image'] = MainImage.objects.filter(name=product['category_name']).first()
        if product['category_guide_image'] is not None:
            product['category_guide_image'] = settings.MEDIA_URL + product['category_guide_image'].image.name

        blog_reivews = helper_get_blog_reviews(product_id)
        magazines = helper_get_product_magazines(product_id)
        magazines_fold = magazines[4:]
        magazines = magazines[:4]

        user = helper_get_user(request)
        user_profile = user.profile

        if user is not None:

            return render(request, 'report_detail.html',
                          {
                              'tab_name': 'myinfo',
                              'next': next,
                              'product': product,
                              'magazines': magazines,
                              'magazines_fold': magazines_fold,
                              'blog_reviews': blog_reivews
                          })

        else:
            logger.error('have_to_login')

    else:
        return render(request, "404.html")


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@csrf_exempt
def mobile_report_form_index_view(request):
    return render(request, 'report_form_index.html',
                  {
                      'next': reverse('mobile_report_form'),
                  })


# 함수 명 그대로의 기능 ( web과 prefix만 다름 )
@mobile_login_required
def mobile_report_form_view(request):
    survey = helper_get_survey_items(request)

    survey_ = []
    survey_group = []
    survey_range = len(survey['survey_items']) + 1

    for i in range(len(survey['survey_items'])):
        survey['survey_items'][i].update({
            'label_index': str(i + 1)
        })
        survey_group.append(survey['survey_items'][i])
        if (i + 1) % 2 == 0:
            survey_.append(survey_group)
            survey_group = []

    if len(survey_group) != 0:
        survey_.append(survey_group)

    return render(request, 'report_form.html',
                  {
                      'next': reverse('mobile_report_form'),
                      'survey': survey_,
                      'survey_id': survey['survey_id'],
                      'survey_range': survey_range
                  })


# user의 survey에 입력한 정보를 서버에 입력하는 api
@csrf_exempt
def request_survey(request):
    data = {
        'survey_id': request.POST.get('survey_id', None),
        'preference_brand': request.POST.get('preference_brand', None),
        'comments': request.POST.get('comments', ''),
        'options': request.POST.getlist('options[]', None)
    }

    if data is None:
        pass
    else:
        helper_request_survey(request, data)
        return http_response_by_json()

    return http_response_by_json(CODE_PARAMS_WRONG)


# 함수 명 그대로의 기능
@csrf_exempt
@login_required
def do_interest_product(request):
    user_id = request.user.id
    product_id = request.POST.get('product_id')
    user_survey_id = request.POST.get('user_survey_id')
    try:
        interest = NInterest.objects.create(user_id=user_id, product_id=product_id, user_survey_id=user_survey_id)
        return http_response_by_json()
    except IntegrityError as e:
        return http_response_by_json(CODE_INTEGRITY_ERROR)


# 함수 명 그대로의 기능
@csrf_exempt
@login_required
def undo_interest_product(request):
    interest_id = request.POST.get('interest_id')
    interest = NInterest.objects.get(pk=interest_id)
    interest.delete()

    return http_response_by_json()


# survey를 다시 할 때 호출되는 page
@csrf_exempt
@login_required
def survey_again(request):
    user_survey_id = request.POST.get('user_survey_id')
    new_user_survey = UserSurvey.objects.filter(id=user_survey_id)[:1][0]
    new_user_survey.pk = None
    new_user_survey.save()
    user_survey = UserSurvey.objects.filter(id=user_survey_id)[:1][0]
    user_survey_detail_list = user_survey.details.all()
    for user_survey_detail in user_survey_detail_list:
        UserSurveyDetail.objects.create(user_survey=new_user_survey,
                                        survey_item_option=user_survey_detail.survey_item_option)

    item = request.POST.get('item')
    reason = request.POST.get('reason')
    comments = request.POST.get('comments')
    try:
        user_survey_again = UserSurveyAgain.objects.create(user_survey=new_user_survey, item=item, reason=reason,
                                                           comments=comments)
        return http_response_by_json()
    except IntegrityError as e:
        return http_response_by_json(CODE_INTEGRITY_ERROR)


# 추가정보 요청 api
@csrf_exempt
@login_required
def request_more(request):
    user_survey_id = request.POST.get('user_survey_id')
    comments = request.POST.get('comments')

    user_survey = UserSurvey.objects.get(pk=user_survey_id)

    try:
        UserSurveyMore.objects.create(user_survey=user_survey, comments=comments)
        return http_response_by_json()
    except IntegrityError as e:
        return http_response_by_json(CODE_INTEGRITY_ERROR)


# 함수 명 그대로의 기능
class SignupView(RedirectAuthenticatedUserMixin, CloseableSignupMixin,
                 AjaxCapableProcessFormViewMixin, FormView):
    template_name = "account/signup.html"
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        # send_mail('subjetc here', 'here is the message', 'from@example.com', ['parkjuram@naver.com'], fail_silently=False)
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'signup', self.form_class)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret

    def form_valid(self, form):
        user = form.save(self.request)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_context_data(self, **kwargs):
        form = kwargs['form']
        form.fields["email"].initial = self.request.session \
            .get('account_verified_email', None)
        ret = super(SignupView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


signup = SignupView.as_view()



# 이메일 인증시 이메일에 있는 활성링크를 눌렀을때 호출되는 페이지
def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        return redirect('index')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        pass
        # return render_to_response('user_profile/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return redirect('index')