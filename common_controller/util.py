from django.conf import settings
from django.http.response import HttpResponse
from web.models import Product, Set, ChangeableProduct, BlogReview, Brand
from users.models import Interest, Cart, Purchase, CustomSet, CustomSetDetail
from django.core.exceptions import ObjectDoesNotExist

from motion9.const import *
import logging
import math
import json

logger = logging.getLogger(__name__)

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

    return HttpResponse(json.dumps(json_, ensure_ascii=False), content_type="application/json; charset=utf-8")

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

def helper_get_products(user=None, category_id=None, price_max_filter=None, price_min_filter=None, brandname_filter=None):

    products = Product.objects
    if category_id is not None:
        products = products.filter(category__id=category_id)

    if price_max_filter is not None and price_min_filter is not None:
        products = products.filter(discount_price__lte=price_max_filter, discount_price__gte=price_min_filter)

    if brandname_filter is not None:
        products = products.filter(brand__id=brandname_filter)

    products = products.all()
    products_ = []

    for product in products:
        product_ = helper_get_product_detail(product, user)
        products_.append(product_)

    return products_

def helper_get_product_detail(product_id_or_object, user=None):

    if isinstance(product_id_or_object, unicode) or isinstance(product_id_or_object, int):
        product_id = product_id_or_object
        product_object = None
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
            # 'big_img_url': product.big_img_url,
            'big_img_url': settings.MEDIA_URL + product.thumbnail_image.name,
            # 'small_img_url': product.small_img_url,
            'small_img_url': settings.MEDIA_URL + product.thumbnail_image.name,
            'video_url': product.description,
            'brandname': product.brandname,
            'maker': product.maker,
            'capacity': product.capacity,
            'original_price': product.original_price,
            'discount_price': product.discount_price,
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
        'name': user.email + str(custom_set.id),
        'category_name': set.category.name,
        'description': set.description,
        'big_img_url': set.custom_big_img_url,
        'small_img_url': set.custom_small_img_url,
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
            product = custom_set_detail.new_product

            original_price += product.original_price
            discount_price += product.discount_price

    custom_set_.update({
        'original_price': original_price,
        'discount_price': discount_price-set.discount_difference
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

    set_ = {}
    set_.update({
        'id': set.id,
        'name': set.name,
        'category_name': set.category.name,
        'description': set.description,
        'big_img_url': set.big_img_url,
        'small_img_url': set.small_img_url,
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

    return set_

def helper_get_custom_set_list(user=None):
    custom_sets = user.get_custom_sets.all()

    custom_sets_ = []

    for custom_set in custom_sets:
        custom_set_ = helper_get_custom_set(custom_set, user)
        custom_sets_.append(custom_set_)
        
    return custom_sets_

def helper_get_set_list(category_id, user, price_max_filter=None, price_min_filter=None):
    sets = Set.objects
    if category_id is not None:
        sets = sets.filter(category__id=category_id)

    sets = sets.all()
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

def helper_add_custom_set_cart(user, custom_set_id, item_count):
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
