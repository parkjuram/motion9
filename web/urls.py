from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^shop/product/$', 'web.views.shop_product_view', name='shop_product'),
    url(r'^shop/product/(?P<category_id>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    url(r'^shop/product/page/(?P<page_num>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),
    url(r'^shop/product/(?P<category_id>(\d+))/(?P<page_num>(\d+))/$', 'web.views.shop_product_view', name='shop_product'),

    url(r'^product/(?P<product_id>(\d+))/$', 'web.views.product_view', name='product'),
    url(r'^product/(?P<product_id>(\d+))/json/$', 'web.views.product_json_view', name='product_json'),

    url(r'^shop/set/$', 'web.views.shop_set_view', name='shop_set'),
    url(r'^shop/set/(?P<category_id>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    url(r'^shop/set/page/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
    url(r'^shop/set/(?P<category_id>(\d+))/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),

    url(r'^set/(?P<set_id>(\d+))/$', 'web.views.set_view', name='set'),

)