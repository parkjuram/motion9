from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^test/$', 'web.views.test_view', name='test'),
    url(r'^$', 'web.views.index_view', name='index'),
    url(r'^index/$', 'web.views.index_view', name='index'),

    url(r'^shop/product/$', 'web.views.shop_product_view', name='shop_product'),
    url(r'^shop/product/(?P<category_id>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    url(r'^shop/product/page/(?P<page_num>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    url(r'^shop/product/(?P<category_id>(\d+))/(?P<page_num>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),

    url(r'^product/(?P<product_id>(\d+))/$', 'web.views.product_view', name='product'),
    url(r'^product/(?P<product_id>(\d+))/json/$', 'web.views.product_json_view', name='product_json'),
    url(r'^product/(?P<product_id>(\d+))/modal/$', 'web.views.product_modal_view', name='product_modal'),

    url(r'^shop/set/$', 'web.views.shop_set_view', name='shop_set'),
    url(r'^shop/set/(?P<category_id>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    url(r'^shop/set/page/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    url(r'^shop/set/(?P<category_id>(\d+))/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),

    url(r'^set/(?P<set_id>(\d+))/$', 'web.views.set_view', name='set'),

    url(r'^customize/set/(?P<set_id>(\d+))/$', 'web.views.customize_set_view', name='customize_set'),
    url(r'^customize/set/save/$', 'web.views.customize_set_save_view', name='customize_set_save'),
)