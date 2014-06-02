from web.models import Product, Set
from django.core.exceptions import ObjectDoesNotExist

import logging

logger = logging.getLogger(__name__)

def helper_get_user(request):
    if request.user and request.user.is_authenticated():
        return request.user
    else:
        return None

def helper_get_product(product_id_or_object, user):

    # if isinstance(product_id_or_object, Product):
    if isinstance(product_id_or_object, int):
        product_id = product_id_or_object
        product_object = None
    elif isinstance(product_id_or_object, Product):
        product_object = product_id_or_object

    try:
        if product_object is None:
            product = Product.objects.get(id=product_id)
        else:
            product = product_object

        product_ = {
            'id': product.id,
            'name': product.name,
            'category_name': product.category.name,
            'description': product.description,
            'big_img_url': product.big_img_url,
            'small_img_url': product.small_img_url,
            'video_url': product.description,
            'brandname': product.brandname,
            'maker': product.maker,
            'capacity': product.capacity,
            'original_price': product.original_price,
            'discount_price': product.discount_price,
            'fit_skin_type': product.fit_skin_type,
            'color_description': product.color_description,
            'color_rgb': product.color_rgb,
            'is_interested': True if user is not None and product.interest_set.filter(user=user).count()>0 else False
        }

        return product_

    except ObjectDoesNotExist as e:
        logger.error(e)

def helper_get_set(set_id, user=None):
    set = Set.objects.get(id=set_id)
    set_ = {}
    set_.update({
        'id': set.id,
        'name': set.name,
        'category_name': set.category.name,
        'description': set.description,
        'big_img_url': set.big_img_url,
        'small_img_url': set.small_img_url,
        'discount_difference': set.discount_difference,
        'products': []
    })

    set_products = set.setproduct_set.all()
    original_price = 0
    discount_price = 0
    for set_product in set_products:
        product = set_product.product

        original_price += product.original_price
        discount_price += product.discount_price

        product_ = helper_get_product( product.id, user)
        set_['products'].append(product_)

    set_.update({
        'original_price': original_price,
        'discount_price': discount_price
    })

    return set_
