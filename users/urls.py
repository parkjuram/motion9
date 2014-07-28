from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^check/email/$', 'users.views.check_email_view', name='check_email'),
    url(r'^check/token/facebook/$', 'users.views.check_facebook_token_view', name='check_facebook_token'),

    url(r'^registration/$', 'users.views.registration', name='registration'),
    url(r'^registration_page/$', 'users.views.registration_view', name='registration_page'),

    url(r'^mobile/registration_page/$', 'users.views.mobile_registration_view', name='mobile_registration_page'),

    url(r'^login/$', 'users.views.login', name='login'),
    url(r'^login/(?P<next>(\w+))/$', 'users.views.login', name='login'),
    url(r'^login_page/$', 'users.views.login_view', name='login_page'),
    url(r'^logout/$', 'users.views.logout_', name='logout'),
    url(r'^update/$', 'users.views.update', name='update'),

    url(r'^mypage/$', 'users.views.mypage_view', name='mypage'),
    url(r'^mypage/(?P<page_num>(\d+))/$', 'users.views.mypage_view', name='mypage'),

    url(r'^mypage/set/$', 'users.views.mypage_set_view', name='mypage_set'),
    url(r'^mypage/set/(?P<page_num>(\d+))/$', 'users.views.mypage_set_view', name='mypage_set'),

    url(r'^mypage/purchase/$', 'users.views.mypage_purchase_view', name='mypage_purchase'),
    url(r'^mypage/purchase/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_view', name='mypage_purchase'),

    url(r'^mypage/purchase/product/$', 'users.views.mypage_purchase_product_view', name='mypage_purchase_product'),
    url(r'^mypage/purchase/product/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_product_view', name='mypage_purchase_product'),

    url(r'^mypage/purchase/set/$', 'users.views.mypage_purchase_set_view', name='mypage_purchase_set'),
    url(r'^mypage/purchase/set/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_set_view', name='mypage_purchase_set'),

    url(r'^mypage/purchase/custom_set/$', 'users.views.mypage_purchase_custom_set_view', name='mypage_purchase_custom_set'),
    url(r'^mypage/purchase/custom_set/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_custom_set_view', name='mypage_purchase_custom_set'),

    url(r'^mypage/cart/$', 'users.views.mypage_cart_view', name='mypage_cart'),
    url(r'^mypage/cart/json/$', 'users.views.mypage_cart_json_view', name='mypage_cart_json'),

    url(r'^interest/add/$', 'users.views.add_interest', name='add_interest'),
    url(r'^interest/del/$', 'users.views.delete_interest', name='del_interest'),

    url(r'^cart/add/$', 'users.views.add_cart', name='add_cart'),
    url(r'^cart/del/$', 'users.views.delete_cart', name='del_cart'),

    url(r'^purchase/add/$', 'users.views.add_purchase', name='add_purchase'),
    url(r'^purchase/del/$', 'users.views.delete_purchase', name='del_purchase'),

    url(r'^custom/$', 'users.views.make_custom_set', name='make_custom_set'),

#     mobile part

    url(r'^mobile/login_page/$', 'users.views.mobile_login_view', name='mobile_login_page'),

    url(r'^mobile/mypage/$', 'users.views.mobile_mypage_view', name='mobile_mypage'),
    url(r'^mobile/mypage/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_view', name='mobile_mypage'),

    url(r'^mobile/mypage/set/$', 'users.views.mobile_mypage_set_view', name='mobile_mypage_set'),
    url(r'^mobile/mypage/set/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_set_view', name='mobile_mypage_set'),

    url(r'^mobile/mypage/before_purchase/$', 'users.views.mobile_mypage_before_purchase_view', name='mobile_mypage_before_purchase'),

    # url(r'^mobile/mypage/purchase/product/$', 'users.views.mobile_mypage_purchase_product_view', name='mobile_mypage_purchase_product'),
    # url(r'^mobile/mypage/purchase/product/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_purchase_product_view', name='mobile_mypage_purchase_product'),
    #
    # url(r'^mobile/mypage/purchase/set/$', 'users.views.mobile_mypage_purchase_set_view', name='mobile_mypage_purchase_set'),
    # url(r'^mobile/mypage/purchase/set/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_purchase_set_view', name='mobile_mypage_purchase_set'),
    #
    # url(r'^mobile/mypage/purchase/custom_set/$', 'users.views.mobile_mypage_purchase_custom_set_view', name='mobile_mypage_purchase_custom_set'),
    # url(r'^mobile/mypage/purchase/custom_set/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_purchase_custom_set_view', name='mobile_mypage_purchase_custom_set'),

    url(r'^mobile/mypage/cart/$', 'users.views.mobile_mypage_cart_view', name='mobile_mypage_cart'),



# @app.route('/mypage/set', methods = ['GET'])
# @app.route('/mypage/set/<int:pageNum>', methods = ['GET'])
# @login_required
# def myPageSetWeb(pageNum=None):

)