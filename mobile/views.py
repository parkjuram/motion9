from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common_controller.util import helper_get_products, helper_get_user, helper_make_paging_data, helper_get_set_list, \
    helper_get_product_detail, helper_get_blog_reviews, http_response_by_json, helper_get_set

from web.models import Category

from motion9.const import *

@csrf_exempt
def index_view(request):
    product_categories = Category.objects.filter(is_set=False).all()
    set_categories = Category.objects.filter(is_set=True).all()

    return render(request, 'index.html',
                  {
                      'product_categories': product_categories,
                      'set_categories': set_categories,
                  })

@csrf_exempt
def purchase_view(request):
    return render(request, 'purchase.html',
                  {
                  })

@csrf_exempt
def shop_product_view(request, category_id=None, page_num=1):

    page_num = int(page_num)

    products_ = helper_get_products(helper_get_user(request), category_id)

    if page_num is not None:
        products_ = helper_make_paging_data(len(products_), products_[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_FOR_PRODUCT], page_num)
    else:
        products_ = {'data': products_}

    categories = Category.objects.filter(is_set=False).all()

    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    return render(request, 'shopping_product.html',
                  {

                      'products': products_,
                      'current_category': current_category,
                      'categories': categories,
                      'current_page': 'shop_product'
                  })

@csrf_exempt
def shop_set_view(request, category_id=None, page_num=1):

    page_num = int(page_num)

    sets = helper_get_set_list(category_id, helper_get_user(request))

    if page_num is not None:
        sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_SET:page_num*ITEM_COUNT_PER_PAGE_FOR_SET], page_num)
    else:
        sets = {'data': sets}

    categories = Category.objects.filter(is_set=True).all()
    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    return render(request, 'shopping_set.html',
                  {
                      'sets': sets,
                      'current_category': current_category,
                      'categories': categories,
                      'current_page': 'shop_set'
                  })

@csrf_exempt
def product_view(request, product_id=None):
    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))
        blog_reivews = helper_get_blog_reviews(product_id)

        return render(request, "product_detail.html",
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
def set_view(request, set_id):
    set = helper_get_set(set_id, helper_get_user(request))

    return render(request, 'set_detail.html',
                {
                    'set': set
                })


@csrf_exempt
def customize_set_view(request, set_id):
    set = helper_get_set(set_id, helper_get_user(request), True)

    return render(request, "change_product_in_set.html",
          {
              'set': set
          })