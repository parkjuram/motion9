from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from motion9.const import *
from web.models import Product, Category, BlogReview

import math
import logging

logger = logging.getLogger(__name__)

# # def get_product_list(page_num=1, category_key=None):
# def getProductList(page_num=1, category_key=None):
#     stmt = g.db.session.query(Interest).filter(Interest.user_key == g.user.key if g.user else -1).subquery()
#
#     query = g.db.session.query(Product, Category.name.label('category_name'), stmt.c.key).\
#         outerjoin(stmt, Product.key == stmt.c.product_key).\
#         filter(Category.key == Product.category_key)
#
#     query = query.filter(Product.category_key == category_key) if category_key is not None else query
#
#     pager_indicator_total_length = int(math.ceil(float(query.count()) / ITEM_COUNT_PER_PAGE))
#     products_and_category_name_and_is_interested = \
#         query.order_by(Product.key).all() \
#         if page_num == 0 else \
#         query.order_by(Product.key).slice((page_num-1)*ITEM_COUNT_PER_PAGE, page_num*ITEM_COUNT_PER_PAGE).all()
#
#     product_list = []
#     for product, category_name, is_interested in products_and_category_name_and_is_interested:
#         product.category_name = category_name
#         product.is_interested = True if is_interested is not None else False
#
#         columns = get_table_columns(Product, ['category_name', 'is_interested'])
#         product_dict = get_dict_from_model(product, columns)
#         product_list.append(product_dict)
#
#     if page_num is not 0:
#         product_list = make_data_to_paging_format_dict(pager_indicator_total_length, page_num, product_list)
#     else:
#         product_list = {'data': product_list}
#
#     return product_list


# def make_data_to_paging_format_dict(pager_indicator_total_length, page_num, data):
#     resp = {}
#     pager_indicator_total_length = 1 if pager_indicator_total_length == 0 else pager_indicator_total_length
#     resp.update({
#         'page_total_count': pager_indicator_total_length,
#         'page_left_count': page_num - (page_num%PAGER_INDICATOR_LENGTH_PER_PAGE) + 1,
#     })
#     resp.update({
#         'page_right_count': pager_indicator_total_length
#         if pager_indicator_total_length < resp['page_left_count'] + PAGER_INDICATOR_LENGTH_PER_PAGE - 1
#         else resp['page_left_count'] + PAGER_INDICATOR_LENGTH_PER_PAGE - 1,
#     })
#     resp.update({
#         'page_hasPrev': True if resp['page_left_count'] is not 1 else False,
#         'page_hasNext': True if resp['page_right_count'] is not pager_indicator_total_length else False,
#         'data': data
#     })
#     return resp

# def getBlogReviewList( product_or_set_key, is_set = False ):
#     if is_set is False:
#         product_key = product_or_set_key
#         blogReviews = g.db.session.query( BlogReview ).filter( BlogReview.product_key == product_key).all()
#     else:
#         set_key = product_or_set_key
#         blogReviews = g.db.session.query( BlogReview ).filter( and_( SetProduct.set_key == set_key, BlogReview.product_key == SetProduct.product_key) ).all()
#
#     return blogReviews

def _get_blog_reviews(product_id):
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

def _get_user(request):
    if request.user and request.user.is_authenticated():
        return request.user
    else:
        return None

def _get_product(product_id, user):
    try:
        product = Product.objects.get(id=product_id)

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


def shop_product_view(request, category_id=None, page_num=None):

    products = Product.objects
    if category_id is not None:
        products.filter(category_id=category_id)

    product_count = products.count()
    products = products.all()
    products_ = []

    for product in products:
        is_interest = False
        if request.user and request.user.is_authenticated():
            if product.interest_set.filter(user=request.user).count()>0:
                is_interest = True

        product_ = {}
        product_.update({
            'id': product.id,
            'name': product.name,
            'is_interest': is_interest,
            'category_name': product.category.name,
            'description': product.description,
            'big_img_url': product.big_img_url,
            'small_img_url': product.small_img_url,
            'video_url': product.video_url,
            'brandname': product.brandname,
            'maker': product.maker,
            'capacity': product.capacity,
            'original_price': product.original_price,
            'discount_price': product.discount_price,
            'fit_skin_type': product.fit_skin_type,
            'color_description': product.color_description,
            'color_rgb': product.color_rgb
        })

        products_.append(product_)

    if page_num is not None:
        pager_total_length = math.ceil(product_count/float(ITEM_COUNT_PER_PAGE))
        products_ = {
            'data': products_,
            'page_total_count': pager_total_length,
            'page_left_count': page_num-(page_num%PAGER_INDICATOR_LENGTH)+1,
            'page_right_count': pager_total_length
            if pager_total_length < page_num-(page_num%PAGER_INDICATOR_LENGTH)+PAGER_INDICATOR_LENGTH
            else page_num-(page_num%PAGER_INDICATOR_LENGTH)+PAGER_INDICATOR_LENGTH,
            }
        products_.update({
            'page_hasPrev': True if products_['page_left_count'] is not 1 else False,
            'page_hasNext': True if products_['page_right_count'] is not pager_total_length else False,
        })
    else:
        products_ = {'data': products_}

    categories = Category.objects.filter(is_set=False).all()

    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    return render(request, 'shopping_product_web.html',
                  {
                      'products': products_,
                      'current_category': current_category,
                      'categories': categories,
                      'current_page': 'shop_product'
                  })

def product_view(request, product_id=None):
    logger.info( 'def product_view(request, product_id=None): start')

    if product_id is not None:
        product = _get_product(product_id, _get_user())
        blog_reivews = _get_blog_reviews(product_id)
    else:
        logger.error( 'product_id is wrong in product_view')

    logger.info( 'def product_view(request, product_id=None): end')

# def productWeb(product_key):
#     product = getProduct(product_key)
#     blogList = getBlogReviewList(product_key, False)
#     return render_template('product_detail_web.html', product=product, blogReviews=blogList)




















# render example
# return render_to_response('shopping_product_web.html',
#               {
#                   'products': products_,
#                   'current_category': current_category,
#                   'categories': categories,
#                   'current_page': 'shop_product'
#               }, RequestContext(request))