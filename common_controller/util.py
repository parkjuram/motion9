# coding=utf-8
from subprocess import call, Popen, PIPE

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
import time
from foradmin.models import Advertisement, SurveyItem, Survey
from web.models import Product, Set, ChangeableProduct, BlogReview, Brand, ProductMagazine, Faq
from users.models import Interest, Cart, Purchase, CustomSet, CustomSetDetail, Payment, BeforePayment, UserSurvey, \
    UserSurveyDetail
from django.core.exceptions import ObjectDoesNotExist

from motion9.const import *
import logging
import math
import json

logger = logging.getLogger(__name__)

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def send_payment_email(payment_id, user):
    plaintext = get_template('email.txt')
    htmly     = get_template('email.html')

    payment = Payment.objects.get(id=payment_id)

    purchase_products = Purchase.objects.filter(payment_id=payment_id, type='p').all()
    products = []
    for purchase_product in purchase_products:
        product = purchase_product.product
        product_ = helper_get_product_detail(product, user)
        product_['item_count'] = purchase_product.item_count
        product_['total_price'] = purchase_product.price
        products.append(product_)

    purchase_sets = Purchase.objects.filter(payment_id=payment_id, type='s').all()
    sets = []
    for purchase_set in purchase_sets:
        set = purchase_set.set
        set_ = helper_get_set(set, user)
        set_['item_count'] = purchase_set.item_count
        set_['total_price'] = purchase_set.price
        sets.append(set_)

    purchase_custom_sets = Purchase.objects.filter(payment_id=payment_id, type='c').all()
    custom_sets = []
    for purchase_custom_set in purchase_custom_sets:
        custom_set = purchase_custom_set.custom_set
        custom_set_ = helper_get_custom_set(custom_set, user)
        custom_set_['item_count'] = purchase_custom_set.item_count
        custom_set_['total_price'] = purchase_custom_set.price
        custom_sets.append(custom_set_)

    payment.total_price = int(payment.mileage) + int(payment.auth_amount)
    payment.auth_date = str(payment.auth_date)
    payment.auth_date = payment.auth_date[:4] + "년 " + payment.auth_date[4:6] + "월 " + payment.auth_date[6:8] + "일 " + payment.auth_date[8:10] + "시 " + payment.auth_date[10:12] + "분 "

    d = Context({
        'products': products,
        'sets': sets,
        'custom_sets': custom_sets,
        'payment': payment,
        'user_': user
    })

    subject, from_email, to = 'Thanks for payments!', "from@example.com", user.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    is_success = msg.send()

    if is_success == 1:
        return http_response_by_json(None)
    else:
        raise Http404


def billgate_put_data(this_data, put_key, put_value):
    vt = None
    if this_data is not None:
        if this_data.has_key(put_key):
            vt = this_data.get(put_key)
    else:
        this_data = {}

    if vt is None:
        vt = []

    vt.append(put_value)
    this_data[put_key] = vt

def billgate_getErrorMessage(error_code):
    if error_code=="080000":
        return "api command error"
    elif error_code=="080001":
        return "메시지 파싱 에러!!"
    elif error_code=="082001":
        return "소켓 연결 에러!!"
    elif error_code=="082002":
        return "소켓 타임아웃 에러!!"
    elif error_code=="083001":
        return "메시지 암호화 에러!!"
    elif error_code=="083002":
        return "메시지 복호화 에러!!"
    elif error_code=="899900":
        return "알수 없는 에러!!"
    elif error_code=="899901":
        return "API 에러 발생!!"

def http_response_by_json(error=None, json_={}):
    if error is None:
        json_.update({
            'success': True
        })
    else:
        json_.update({
            'success': False,
            'message': ERROR_CODE_AND_MESSAGE_DICT[error],
        })

    return HttpResponse(json.dumps(json_, ensure_ascii=True), content_type="application/json; charset=utf-8")

def helper_get_purchase_status(status):
    if status == 'b':
        return '상품 준비중'
    elif status == 'r':
        return '배송대기'
    elif status == 's':
        return '배송중'
    elif status == 'f':
        return '배송완료'
    return ''

def helper_get_user(request):
    if request.user and request.user.is_authenticated():
        return request.user
    else:
        return None

def helper_get_blog_reviews(product_id):
    blog_reviews = BlogReview.objects.filter(product__id=product_id)

    blog_reviews_ = []
    for blog_review in blog_reviews:
        blog_review_ = {}
        blog_review_.update({
            'writer': blog_review.writer,
            'url': blog_review.url,
            'big_img_url': blog_review.big_img_url,
            'small_img_url': blog_review.small_img_url,
            'review_created_time': blog_review.review_created_time,
            'summary': blog_review.summary,
        })

        blog_reviews_.append(blog_review_)

    return blog_reviews_

def helper_get_product_magazines(product_id):
    product_magazines = ProductMagazine.objects.filter(product_id=product_id)

    product_magazines_ = []
    for product_magazine in product_magazines:
        product_magazine_ = {}
        magazine = product_magazine.magazine
        product_magazine_.update({
            'title': product_magazine.title,
            'magazine_title': magazine.title,
            'author': product_magazine.author,
            'year': product_magazine.year,
            'month': product_magazine.month,
            'link': product_magazine.link
        })
        product_magazines_.append(product_magazine_)

    return product_magazines_

def helper_get_products(user=None, category_id=None, price_max_filter=None, price_min_filter=None, brandname_filter=None):

    products = Product.objects
    if category_id is not None:
        products = products.filter(category__id=category_id)

    if price_max_filter is not None and price_min_filter is not None:
        products = products.filter(discount_price__lte=price_max_filter, discount_price__gte=price_min_filter)

    if brandname_filter is not None:
        products = products.filter(brand__id=brandname_filter)

    products = products.filter(is_active=True).all()
    products_ = []

    for product in products:
        product_ = helper_get_product_detail(product, user)
        products_.append(product_)

    return products_

def helper_get_product_detail(product_id_or_object, user=None):

    if isinstance(product_id_or_object, unicode) or isinstance(product_id_or_object, int):
        product_object = None
        product_id = product_id_or_object
    elif isinstance(product_id_or_object, Product):
        product_object = product_id_or_object

    try:
        if product_object is None:
            product = Product.objects.get(id=product_id)
        else:
            product = product_object

        product_images = product.product_image_set.all()
        images = []
        for product_image in product_images:
            images.append( settings.MEDIA_URL + product_image.image.name)

        product_ = {
            'id': product.id,
            'name': product.name,
            'category_name': product.category.name,
            'description': product.description,
            'images': images,
            'big_img_url': settings.MEDIA_URL + product.thumbnail_image.name,
            'small_img_url': settings.MEDIA_URL + product.thumbnail_image.name,
            'video_url': product.description,
            'brandname': product.brand.name_eng if product.brand.is_repr_to_eng is True else product.brand.name_kor,
            'maker': product.maker,
            'country': product.country,
            'capacity': product.capacity,
            'short_desc': product.short_desc,
            'use_expired_date': product.use_expired_date,
            'production_date': product.production_date,
            'usage': product.usage,
            'ingredient': product.ingredient,
            'judge_result': product.judge_result,
            'precautions': product.precautions,
            'quality_guarantee_standard': product.quality_guarantee_standard,
            'original_price': product.original_price,
            'discount_price': product.discount_price,
            'discount_rate' : round(float(product.original_price-product.discount_price)/product.original_price*100,1) if product.original_price is not 0 else 0,
            'fit_skin_type': product.fit_skin_type,
            'is_interested': True if user is not None and product.interest_set.filter(user=user).count()>0 else False,
            'contains_set': []
        }

        set_products = product.setproduct_set.all()
        for set_product in set_products:
            set = set_product.set
            set_ = helper_get_set(set, user, False, False)
            product_['contains_set'].append(set_)

        return product_

    except ObjectDoesNotExist as e:
        logger.error(e)

# def helper_get_products(user=None, category_id=None, price_max_filter=None, price_min_filter=None, brandname_filter=None):
def helper_get_custom_set(custom_set_id_or_object, user=None):

    if isinstance(custom_set_id_or_object, unicode) or isinstance(custom_set_id_or_object, int):
        custom_set_id = custom_set_id_or_object
        custom_set_object = None
    elif isinstance(custom_set_id_or_object, CustomSet):
        custom_set_object = custom_set_id_or_object

    if custom_set_object is None:
        custom_set = CustomSet.objects.get(id=custom_set_id)
    else:
        custom_set = custom_set_object

    set = custom_set.set

    custom_set_ = {}
    custom_set_.update({
        'id': custom_set.id,
        'name': set.name+"(My Collection)",
        'category_name': set.category.name,
        'description': set.description,
        'big_img_url': settings.MEDIA_URL + set.big_img.name,
        'discount_difference': set.discount_difference,
        'products': []
    })

    set_products = set.setproduct_set.all()
    original_price = 0
    discount_price = 0
    for set_product in set_products:
        product = set_product.product
        if product.get_custom_set_detail_from_original_product.filter(custom_set=custom_set).count() > 0:
            custom_set_detail = product.get_custom_set_detail_from_original_product.filter(custom_set=custom_set).first()
            product = helper_get_product_detail(custom_set_detail.new_product, user)
            custom_set_['products'].append(product)

            original_price += product['original_price']
            discount_price += product['discount_price']

    custom_set_.update({
        'original_price': original_price,
        'discount_price': discount_price-set.discount_difference
    })

    custom_set_.update({
        'discount_rate' : round(float(custom_set_['original_price']-custom_set_['discount_price'])/custom_set_['original_price']*100,1)  if custom_set_['original_price'] is not 0 else 0
    })

    return custom_set_


def helper_get_set(set_id_or_object, user=None, with_custom_info=False, with_detail_info=True):

    if isinstance(set_id_or_object, unicode) or isinstance(set_id_or_object, int):
        set_id = set_id_or_object
        set_object = None
    elif isinstance(set_id_or_object, Set):
        set_object = set_id_or_object

    if set_object is None:
        set = Set.objects.get(id=set_id)
    else:
        set = set_object

    description_images = set.setdescriptionimage_set.values_list('image', flat=True)
    description_images = map(lambda x:settings.MEDIA_URL+x, description_images)

    small_description_images = set.setdescriptionimage_set.values_list('small_image', flat=True)
    small_description_images = map(lambda x:settings.MEDIA_URL+x, small_description_images)

    if set.big_img.name is not None:
        big_img = settings.MEDIA_URL + set.big_img.name
    else:
        big_img = ''

    if set.small_img.name is not None:
        small_img = settings.MEDIA_URL + set.small_img.name
    else:
        small_img = ''


    set_ = {}
    set_.update({
        'id': set.id,
        'name': set.name,
        'category_name': set.category.name,
        'description': set.description,
        'description_detail': set.description_detail,
        'displayed_category_text': set.displayed_category_text,
        'description_images': description_images,
        'small_description_images': small_description_images,
        'big_img_url': big_img,
        'small_img': small_img,
        'discount_difference': set.discount_difference,
        'is_interested': True if user is not None and set.interest_set.filter(user=user).count()>0 else False,
        'products': []
    })

    set_products = set.setproduct_set.all()
    original_price = 0
    discount_price = 0
    for set_product in set_products:
        product = set_product.product

        original_price += product.original_price
        discount_price += product.discount_price

        if with_detail_info:
            product_ = helper_get_product_detail( product.id, user)

            if with_custom_info:
                try:
                    changeable_product = ChangeableProduct.objects.get(set_id=set_id, product_id=product.id)
                    changeable_product_infos = changeable_product.changeableproductinfo_set.all()

                    changeable_products = []
                    for changeable_product_info in changeable_product_infos:
                        changeable_product_ = helper_get_product_detail(changeable_product_info.product, user)
                        changeable_products.append(changeable_product_)

                    product_.update({
                        'is_changeable': True,
                        'changeable_products': changeable_products
                    })

                except Exception as e:
                    product_.update({
                        'is_changeable': False
                    })

            set_['products'].append(product_)

    set_.update({
        'original_price': original_price,
        'discount_price': discount_price-set.discount_difference
    })

    set_.update({
        'discount_rate': round(float(set_['original_price']-set_['discount_price'])/set_['original_price']*100,1) if set_['original_price'] is not 0 else 0
    })

    return set_

def helper_get_custom_set_list(user=None):
    custom_sets = user.get_custom_sets.filter(is_active=True).all()

    custom_sets_ = []

    for custom_set in custom_sets:
        custom_set_ = helper_get_custom_set(custom_set, user)
        custom_sets_.append(custom_set_)
        
    return custom_sets_

def helper_get_set_list(category_id, user, price_max_filter=None, price_min_filter=None):
    sets = Set.objects
    if category_id is not None:
        sets = sets.filter(category__id=category_id)

    sets = sets.filter(is_active=True).order_by('category__id', 'name').all()
    sets_ = []

    for set in sets:
        set_ = helper_get_set(set, user)
        if price_max_filter is not None and price_min_filter is not None:
            if int(set_['discount_price']) <= int(price_max_filter) and int(set_['discount_price']) >= int(price_min_filter):
                sets_.append(set_)
        else:
            sets_.append(set_)

    return sets_



def helper_make_paging_data( all_object_length, lists, item_count_per_page, current_page_num):
    pager_total_length = int(math.ceil( all_object_length/float(item_count_per_page)))
    lists = {
        'data': lists,
        'page_total_count': pager_total_length,
        'page_left_count': current_page_num-( (current_page_num-1)%PAGER_INDICATOR_LENGTH +1 ) +1
    }
    lists.update({
        'page_right_count': lists['page_left_count']+PAGER_INDICATOR_LENGTH-1
        if pager_total_length > lists['page_left_count']+PAGER_INDICATOR_LENGTH-1
        else int(pager_total_length)
    })

    lists.update({
        'page_hasPrev': True if lists['page_left_count'] is not 1 else False,
        'page_hasNext': True if lists['page_right_count'] is not pager_total_length else False,
        'page_range': range(lists['page_left_count'], lists['page_right_count']+1),
        'page_num': current_page_num
    })
    return lists

def helper_get_profile_item(request):
    phone_number = request.user.profile.phone
    phones = phone_number.split('-')
    if len(phones)==3:
        return {
            'phone1': phones[0],
            'phone2': phones[1],
            'phone3': phones[2],
        }
    return None


def helper_put_order_id_in_cart(user, order_id):
    user.cart_set.update(order_id=order_id)

def helper_get_cart_items(user, order_id=None):

    if order_id is not None:
        user.cart_set.update(order_id=order_id)

    if user is not None:
        total_price = 0
        product_carts= user.cart_set.filter(type='p').all()
        products = []
        for product_cart in product_carts:
            product = product_cart.product
            product_ = helper_get_product_detail(product, user)
            product_['cart_id'] = product_cart.id
            product_['item_count'] = product_cart.item_count
            product_['total_price'] = int(product_['discount_price'])*product_cart.item_count
            total_price += product_['total_price']
            products.append(product_)

        set_carts = user.cart_set.filter(type='s').all()
        sets = []
        for set_cart in set_carts:
            set = set_cart.set
            set_ = helper_get_set(set,user)
            set_['cart_id'] = set_cart.id
            set_['item_count'] = set_cart.item_count
            set_['total_price'] = int(set_['discount_price'])*set_cart.item_count
            total_price += set_['total_price']
            sets.append(set_)

        custom_set_carts = user.cart_set.filter(type='c').all()
        custom_sets = []
        for custom_set_cart in custom_set_carts:
            custom_set = custom_set_cart.custom_set
            custom_set_ = helper_get_custom_set(custom_set, user)
            custom_set_['cart_id'] = custom_set_cart.id
            custom_set_['item_count'] = custom_set_cart.item_count
            custom_set_['total_price'] = int(custom_set_['discount_price'])*custom_set_cart.item_count
            total_price += custom_set_['total_price']
            custom_sets.append(custom_set_)

        return { 'products': products,
                'sets': sets,
                'custom_sets': custom_sets,
                'total_price': total_price }

    return None

def helper_update_cart_items_count(user, id_list, count_list, type ):
    for i in range(len(id_list)):
        if type == 'p':
            user.cart_set.filter(product__id=id_list[i], type='p').update(item_count=count_list[i])
        elif type == 's':
            user.cart_set.filter(set__id=id_list[i], type='s').update(item_count=count_list[i])
        elif type == 'c':
            user.cart_set.filter(custom_set__id=id_list[i], type='c').update(item_count=count_list[i])

# interest

def helper_add_product_interest(user, product_id):
    try:
        Interest.objects.create(user=user, product_id=product_id, type='p')
    except Exception as e:
        logger.error(e)

def helper_add_set_interest(user, set_id):
    try:
        Interest.objects.create(user=user, set_id=set_id, type='s')
    except Exception as e:
        logger.error(e)

def helper_delete_product_interest(user, product_id):
    try:
        interest = Interest.objects.get(user=user, product_id=product_id, type='p')
        interest.delete()
    except Exception as e:
        logger.error(e)

def helper_delete_set_interest(user, set_id):
    try:
        interest = Interest.objects.get(user=user, set_id=set_id, type='s')
        interest.delete()
    except Exception as e:
        logger.error(e)

# cart

def helper_add_product_cart(user, product_id, item_count):
    try:
        if Cart.objects.filter(user=user, product_id=product_id, type='p').exists():
            cart = Cart.objects.filter(user=user, product_id=product_id, type='p').first()
            cart.item_count = int(cart.item_count) + item_count
            cart.save()
        else:
            Cart.objects.create(user=user, product_id=product_id, type='p', item_count = item_count)
    except Exception as e:
        logger.error(e)

def helper_add_set_cart(user, set_id, item_count):
    try:
        if Cart.objects.filter(user=user, set_id=set_id, type='s').exists():
            cart = Cart.objects.filter(user=user, set_id=set_id, type='s').first()
            cart.item_count = int(cart.item_count) + item_count
            cart.save()
        else:
            Cart.objects.create(user=user, set_id=set_id, type='s', item_count = item_count)
    except Exception as e:
        logger.error(e)

def helper_add_custom_set_cart(user, custom_set_id, item_count=1):
    try:
        if Cart.objects.filter(user=user, custom_set_id=custom_set_id, type='c').exists():
            cart = Cart.objects.filter(user=user, custom_set_id=custom_set_id, type='c').first()
            cart.item_count = int(cart.item_count) + item_count
            cart.save()
        else:
            Cart.objects.create(user=user, custom_set_id=custom_set_id, type='c', item_count = item_count)
    except Exception as e:
        logger.error(e)

def helper_delete_product_cart(user, product_id):
    try:
        cart = Cart.objects.get(user=user, product_id=product_id, type='p')
        cart.delete()
    except Exception as e:
        logger.error(e)

def helper_delete_set_cart(user, set_id):
    try:
        cart = Cart.objects.get(user=user, set_id=set_id, type='s')
        cart.delete()
    except Exception as e:
        logger.error(e)

def helper_delete_custom_set_cart(user, custom_set_id):
    try:
        cart = Cart.objects.get(user=user, custom_set_id=custom_set_id, type='c')
        cart.delete()
    except Exception as e:
        logger.error(e)

# purchase

def helper_add_product_purchase(user, address, product_id):
    try:
        Purchase.objects.create(user=user, address=address, product_id=product_id, type='p')
    except Exception as e:
        logger.error(e)

def helper_add_set_purchase(user, address, set_id):
    try:
        Purchase.objects.create(user=user, address=address, set_id=set_id, type='s')
    except Exception as e:
        logger.error(e)

def helper_add_custom_set_purchase(user, address, custom_set_id):
    try:
        Purchase.objects.create(user=user, address=address, custom_set_id=custom_set_id, type='c')
    except Exception as e:
        logger.error(e)

def helper_delete_product_purchase(user, address, product_id):
    try:
        purchase = Purchase.objects.get(user=user, product_id=product_id, type='p')
        purchase.delete()
    except Exception as e:
        logger.error(e)

def helper_delete_set_purchase(user, address, set_id):
    try:
        purchase = Purchase.objects.get(user=user, set_id=set_id, type='s')
        purchase.delete()
    except Exception as e:
        logger.error(e)

def helper_delete_custom_set_purchase(user, address, custom_set_id):
    try:
        purchase = Purchase.objects.get(user=user, custom_set_id=custom_set_id, type='c')
        purchase.delete()
    except Exception as e:
        logger.error(e)

def helper_get_brands():
    brands = Brand.objects.all()
    brands_ = []
    for brand in brands:
        if brand.is_repr_to_eng:
            name = brand.name_eng
        else:
            name = brand.name_kor

        brand_ = {
            'id': brand.id,
            'name': name
        }

        brands_.append(brand_)


    return brands_


# custom set

def helper_make_custom_set(user, set_id, original_product_id, new_product_id):
    custom_set, created = CustomSet.objects.get_or_create(user=user, set_id=set_id)
    if CustomSetDetail.objects.filter(custom_set=custom_set, original_product_id=original_product_id).exists():
        custom_set_detail = CustomSetDetail.objects.get(custom_set=custom_set, original_product_id=original_product_id)
        custom_set_detail.new_product_id=new_product_id
        custom_set_detail.save()
    else:
        CustomSetDetail.objects.create(custom_set=custom_set, original_product_id=original_product_id, new_product_id=new_product_id)

def helper_get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')

    return user_ip

def helper_get_payment_item(request, total_price, is_mobile=False):

    user = request.user

    current_datetime = time.strftime("%Y%m%d%H%M%S")
    order_id = current_datetime+'_'+str(user.id)
    service_id = 'M1406684' # TEST:'glx_api', REAL:'M1406684'
    order_date = current_datetime
    item_code = str(user.id)+"_"+current_datetime[8:]
    amount = str(total_price)
    user_ip = helper_get_user_ip(request)
    if is_mobile:
        return_url = request.build_absolute_uri(reverse('payment_return_mobile_web'))
    else:
        return_url = request.build_absolute_uri(reverse('payment_return'))
    using_type = '0000'
    currency = '0000'
    installment_period = '0'
    # get checksum
    checksum = helper_get_billgate_payment_checksum(service_id+order_id+amount)

    if checksum=='8001' or checksum=='8003' or checksum=='8009':
        return None
        # return HttpResponse('error code : '+checksum+' \nError Message: make checksum error! Please contact your system administrator!')

    payment_items = {
        'service_id': service_id,
        'order_id': order_id,
        'order_date': order_date,
        'user_id': user.username,
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

    return payment_items

def helper_get_billgate_payment_checksum(temp):
    checksum_command = 'java -cp ./libs/jars/billgateAPI.jar com.galaxia.api.util.ChecksumUtil ' + 'GEN ' + temp
    checksum = (Popen(checksum_command.split(' '), stdout=PIPE).communicate()[0]).strip()

    return checksum

def helper_get_type_name(type):
    type_name=''
    if type=='p':
        type_name='제품'
    elif type=='s':
        type_name='세트'
    elif type=='c':
        type_name='커스텀'

    return type_name

def helper_get_payment_complete_item(request, payment_id):
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
        send_payment_email(payment_id, request.user)
        BeforePayment.objects.filter(order_id=payment.order_id).delete()

    return {
        'products': products,
        'sets': sets,
        'custom_sets': custom_sets,
        'payment': payment,
        'user_': request.user
    }

def helper_get_adarea_items(request):
    advertisements = Advertisement.objects.all()
    adarea_items = []
    for advertisement in advertisements:
        adarea_items.append( {
            'title': advertisement.title,
            'category_id': advertisement.category_id,
            'image_url': ( settings.MEDIA_URL + advertisement.mobile_image.name ) if request.is_mobile else ( settings.MEDIA_URL + advertisement.image.name )
        })

    return adarea_items

def helper_get_purchase_items(request):
    items = []

    purchase_list = request.user.purchase_set.all()
    for purchase in purchase_list:
        if purchase.type == 'p':
            product_dict = model_to_dict(purchase.product)
            product_dict['brandname'] = purchase.product.brand.name_eng if purchase.product.brand.is_repr_to_eng is True else purchase.product.brand.name_kor
            items.append(product_dict)
        elif purchase.type == 's':
            items.append(model_to_dict(purchase.set))
        elif purchase.type == 'c':
            items.append(model_to_dict(purchase.custom_set))

        item = items.pop()
        item['purchase'] = purchase
        item['total_price'] = purchase.price * purchase.item_count
        item['type_name'] = helper_get_type_name(purchase.type)
        item['status_name'] = helper_get_purchase_status(purchase.payment.status)
        item['datetime'] = purchase.payment.auth_date[:4]+"/"+purchase.payment.auth_date[4:6]+"/"+purchase.payment.auth_date[6:8]+"\n"+purchase.payment.auth_date[8:10]+":"+purchase.payment.auth_date[10:12]
        items.append(item)

    return items

def helper_get_faq_items(request):
    faq_items = Faq.objects.filter(is_active=True).order_by('id').values()

    return faq_items

def helper_get_survey_items(request):
    survey = Survey.objects.last()
    survey_items = survey.items.all()

    survey_items_ = []
    for item in survey_items:
        item_ = {}
        options = item.options.order_by('order').values('id', 'content')
        item_.update( {
            'question': item.question,
            'type': item.type,
            'options': options
        })
        survey_items_.append(item_)

    return {
        'survey_id': survey.id,
        'survey_items': survey_items_
    }

def helper_request_survey(request, data):

    user_survey = UserSurvey.objects.create(user=request.user, survey_id=int(data['survey_id']), preference_brand=data['preference_brand'], comments=data['comments'] )

    for option in data['options']:
        UserSurveyDetail.objects.create(user_survey=user_survey, survey_item_option_id=option)


def helper_get_survey_list(request):

    survey_list = request.user.get_survey_list.all()
    return survey_list

def helper_get_survey_result_item(request, survey_id):
    survey_item = request.user.get_survey_list.filter(id=survey_id).values()[0]
    return survey_item

def helper_get_report_count(request):
    report_count = UserSurvey.objects.count()
    return report_count

def convert_skintype_key_to_value(str):
    key_value_pair_list = [
        {'key':'d', 'value':'건성' },
        {'key':'o', 'value':'지성' },
        {'key':'n', 'value':'중성' },
        {'key':'c', 'value':'복합성' },
    ]
    ret = ""
    for key_value_pair in key_value_pair_list:
        if key_value_pair['key'] in str:
            ret += "["+key_value_pair['value']+"]"

    return ret

def convert_feature_key_to_value(str):
    key_value_pair_list = [
        {'key':'wh', 'value':'미백' },
        {'key':'wr', 'value':'주름개선' },
        {'key':'tr', 'value':'트러블' }, # will be deleted
        {'key':'su', 'value':'자외선차단' },
        {'key':'no', 'value':'특징 없음' },
    ]
    ret = ""
    for key_value_pair in key_value_pair_list:
        if key_value_pair['key'] in str:
            ret += "["+key_value_pair['value']+"]"

    return ret