# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from common_controller.decorators import mobile_login_required

from common_controller.util import helper_get_products, helper_get_user, helper_make_paging_data, helper_get_set_list, \
    helper_get_product_detail, helper_get_blog_reviews, http_response_by_json, helper_get_set, helper_get_product_magazines, \
    helper_get_custom_set_list, helper_get_custom_set, helper_get_payment_complete_item, helper_get_adarea_items, \
    helper_get_faq_items, helper_get_survey_list, helper_get_survey_result_item
from foradmin.models import MainImage, Advertisement, Preference
from motion9 import settings
from users.models import Payment

from web.models import Category

from motion9.const import *

@csrf_exempt
def index_view(request):
    # category_images = Category.objects.filter(is_set=True).all()
    # category_images = list(map(lambda x:settings.MEDIA_URL+x.small_image.name, category_images))
    # main_image = settings.MEDIA_URL + MainImage.objects.get(name='main').image.name


    product_categories = Category.objects.filter(is_set=False).all()
    set_categories = Category.objects.filter(is_set=True).all()

    main_image = MainImage.objects.filter(name='Main_m').all()[0]
    main_image_url = settings.MEDIA_URL + main_image.image.name
    #
    # set_category_images_row = []
    try:
        set_categorys = Category.objects.filter(is_set=True).all()

        set_category_images = []
        for set_category in set_categorys:
            set_category_images.append( {
                'id': set_category.id,
                'image_url': settings.MEDIA_URL + set_category.small_image.name
            })

    except:
        pass


    main_notice = Preference.objects.filter(name='MainNotice').first()

    return render(request, 'index.html',
                  {
                      'product_categories': product_categories,
                      'set_categories': set_categories,
                      'main_image_url': main_image_url,
                      'set_category_images': set_category_images,
                      'main_notice': main_notice
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
        products_ = helper_make_paging_data(len(products_), products_[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_PRODUCT:page_num*ITEM_COUNT_PER_PAGE_FOR_PRODUCT], ITEM_COUNT_PER_PAGE_FOR_PRODUCT, page_num)
    else:
        products_ = {'data': products_}

    categories = Category.objects.filter(is_set=False).all()

    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    adarea_items = helper_get_adarea_items(request)

    return render(request, 'shopping_product.html',
                  {

                      'products': products_,
                      'current_category': current_category,
                      'current_category_id': category_id,
                      'categories': categories,
                      'current_page': 'shop_product',
                      'adarea_items': adarea_items
                  })

@csrf_exempt
def shop_set_view(request, category_id=None, page_num=1):

    page_num = int(page_num)

    sets = helper_get_set_list(category_id, helper_get_user(request))

    if page_num is not None:
        sets = helper_make_paging_data(len(sets), sets[(page_num-1)*ITEM_COUNT_PER_PAGE_FOR_SET:page_num*ITEM_COUNT_PER_PAGE_FOR_SET], ITEM_COUNT_PER_PAGE_FOR_SET, page_num)
    else:
        sets = {'data': sets}

    categories = Category.objects.filter(is_set=True).all()
    if category_id is None:
        current_category = 'all'
    else:
        current_category = Category.objects.get(id=category_id).name

    adarea_items = helper_get_adarea_items(request)

    return render(request, 'shopping_set.html',
                  {
                      'sets': sets,
                      'current_category': current_category,
                      'current_category_id': category_id,
                      'categories': categories,
                      'current_page': 'shop_set',
                      'adarea_items': adarea_items
                  })

@csrf_exempt
def product_view(request, product_id=None):
    if product_id is not None:
        product = helper_get_product_detail(product_id, helper_get_user(request))

        product['category_guide_image'] = MainImage.objects.filter(name=product['category_name']).first()
        if product['category_guide_image'] is not None:
            product['category_guide_image'] = settings.MEDIA_URL + product['category_guide_image'].image.name


        blog_reivews = helper_get_blog_reviews(product_id)
        magazines = helper_get_product_magazines(product_id)
        magazines_fold = magazines[4:]
        magazines = magazines[:4]

        return render(request, "product_detail.html",
                      {
                          'product': product,
                          'magazines': magazines,
                          'magazines_fold': magazines_fold,
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

@mobile_login_required
@csrf_exempt
def customize_set_make_view(request, set_id):
    set = helper_get_set(set_id, helper_get_user(request), True)

    return render(request, "change_product_in_set.html",
          {
              'set': set
          })

@mobile_login_required
@csrf_exempt
def customize_set_view(request):
    custom_sets = helper_get_custom_set_list(helper_get_user(request))

    return render(request, "shopping_custom.html",
          {
              'custom_sets': custom_sets
          })

    # set =

@csrf_exempt
def customize_set_detail_view(request, set_id):
    custom_set = helper_get_custom_set(set_id, helper_get_user(request))

    return render(request, "custom_detail.html",
          {
              'custom_set': custom_set
          })

@mobile_login_required
@csrf_exempt
def payment_complete_view(request, payment_id=None):
    if payment_id == None:
        return http_response_by_json(CODE_PARAMS_WRONG)

    payment_complete_item = helper_get_payment_complete_item(request, payment_id)

    return render(request, 'payment_complete.html', payment_complete_item)

def ship_view(request):
    return render(request, 'ship.html')

def mobile_faq_view(request):
    faq_items = helper_get_faq_items(request)

    return render(request, 'faq.html', {
        'faq_items': faq_items
    })


def agreement_of_utilization_view(request):
    service = Preference.objects.filter(name='Service').first()

    return render(request, 'agreement_of_utilization.html', {
        'service': service
    })

def privacy_view(request):
    privacy = Preference.objects.filter(name='Privacy').first()

    return render(request, 'privacy.html', {
        'privacy': privacy
    })


@mobile_login_required
def survey_list_view(request):
    survey_list = helper_get_survey_list(request)
    for item in survey_list:
        if len(item['result_file_name'])==0:
            item['is_analysis_finish'] = False
        else:
            item['is_analysis_finish'] = True

        item['display_name'] = item['created'].strftime("%Y년 %m월 %d일") + " 분석 보고서 (분석중)" if item['is_analysis_finish'] == False else ""

    return render(request, 'survey_list.html', {
        'survey_list': survey_list
    })

@mobile_login_required
def survey_result_view(request, pk):
    survey_result_item = helper_get_survey_result_item(request, pk)
    return render(request, 'survey_result.html', {
        'survey_result_item': survey_result_item
    })
