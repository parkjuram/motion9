from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'mobile.views.index_view', name='mobile_index'),
    url(r'^index/$', 'mobile.views.index_view', name='mobile_index'),
    url(r'^purchase/$', 'mobile.views.purchase_view', name='mobile_purchase'),

    url(r'^shop/product/$', 'mobile.views.shop_product_view', name='mobile_shop_product'),
    url(r'^shop/product/(?P<category_id>(\d+))/$', 'mobile.views.shop_product_view', name='mobile_shop_product'),
    url(r'^shop/product/page/(?P<page_num>(\d+))/$', 'mobile.views.shop_product_view', name='mobile_shop_product'),
    url(r'^shop/product/(?P<category_id>(\d+))/page/(?P<page_num>(\d+))/$', 'mobile.views.shop_product_view', name='mobile_shop_product'),

    url(r'^product/(?P<product_id>(\d+))/$', 'mobile.views.product_view', name='mobile_product'),
    url(r'^product/(?P<product_id>(\d+))/json/$', 'mobile.views.product_json_view', name='mobile_product_json'),
    url(r'^product/(?P<product_id>(\d+))/modal/$', 'mobile.views.product_modal_view', name='mobile_product_modal'),

    url(r'^shop/set/$', 'mobile.views.shop_set_view', name='mobile_shop_set'),
    url(r'^shop/set/(?P<category_id>(\d+))/$', 'mobile.views.shop_set_view', name='mobile_shop_set'),
    url(r'^shop/set/page/(?P<page_num>(\d+))/$', 'mobile.views.shop_set_view', name='mobile_shop_set'),
    url(r'^shop/set/(?P<category_id>(\d+))/page/(?P<page_num>(\d+))/$', 'mobile.views.shop_set_view', name='mobile_shop_set'),

    url(r'^set/(?P<set_id>(\d+))/$', 'mobile.views.set_view', name='mobile_set'),

    url(r'^customize/set/make/(?P<set_id>(\d+))/$', 'mobile.views.customize_set_make_view', name='mobile_customize_set_make'),
    url(r'^customize/set/$', 'mobile.views.customize_set_view', name='mobile_customize_set'),
    url(r'^customize/set/(?P<set_id>(\d+))/$', 'mobile.views.customize_set_detail_view', name='mobile_customize_set_detail'),
    # url(r'^customize/set/save/$', 'mobile.views.customize_set_save_view', name='mobile_customize_set_save'),

    url(r'^payment/complete/$', 'mobile.views.payment_complete_view', name='mobile_payment_complete'),
    url(r'^payment/complete/(?P<payment_id>(\d+))/$', 'mobile.views.payment_complete_view', name='mobile_payment_complete'),

    # url(r'^test/$', 'web.views.test_view', name='test'),
    # url(r'^$', 'web.views.index_view', name='index'),
    # url(r'^index/$', 'web.views.index_view', name='index'),
    #
    # url(r'^shop/product/$', 'web.views.shop_product_view', name='shop_product'),
    # url(r'^shop/product/(?P<category_id>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    # url(r'^shop/product/page/(?P<page_num>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    # url(r'^shop/product/(?P<category_id>(\d+))/page/(?P<page_num>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    #
    # url(r'^product/(?P<product_id>(\d+))/$', 'web.views.product_view', name='product'),
    # url(r'^product/(?P<product_id>(\d+))/json/$', 'web.views.product_json_view', name='product_json'),
    # url(r'^product/(?P<product_id>(\d+))/modal/$', 'web.views.product_modal_view', name='product_modal'),
    #
    # url(r'^shop/set/$', 'web.views.shop_set_view', name='shop_set'),
    # url(r'^shop/set/(?P<category_id>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    # url(r'^shop/set/page/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    # url(r'^shop/set/(?P<category_id>(\d+))/page/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    #
    # url(r'^set/(?P<set_id>(\d+))/$', 'web.views.set_view', name='set'),
    #
    # url(r'^customize/set/(?P<set_id>(\d+))/$', 'web.views.customize_set_view', name='customize_set'),
    # url(r'^customize/set/save/$', 'web.views.customize_set_save_view', name='customize_set_save'),
)