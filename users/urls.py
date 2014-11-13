from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^check/email/$', 'users.views.check_email_view', name='check_email'),

    url(r'^check/email/$', 'users.views.check_email_view', name='check_email'),
    url(r'^check/token/facebook/$', 'users.views.check_facebook_token_view', name='check_facebook_token'),
    url(r'^check/token/facebook/(?P<next>(\w+))/fail/(?P<fail>(\w+))/$', 'users.views.check_facebook_token_view', name='check_facebook_token'),

    url(r'^registration/(?P<next>([\w:/#]+))/$', 'users.views.registration', name='registration'),
    url(r'^registration_page/$', 'users.views.registration_view', name='registration_page'),

    url(r'^mobile/registration_page/$', 'users.views.mobile_registration_view', name='mobile_registration_page'),

    url(r'^login/$', 'users.views.login_', name='login'),
    url(r'^login/(?P<next>.*?)/$', 'users.views.login_', name='login'),
    url(r'^login_page/$', 'users.views.login_view', name='login_page'),
    # url(r'^login_page/(?P<next>.*?)/$', 'users.views.login_view', name='login_page'),
    url(r'^logout/$', 'users.views.logout_', name='logout'),
    # url(r'^logout/(?P<next>(\w+))/$', 'users.views.logout_', name='logout'),
    url(r'^accounts/modify/$', 'users.views.account_modify_view', name='account_modify'),
    url(r'^update/(?P<next>(\w+))/$', 'users.views.update', name='update'),

    url(r'^mypage/$', 'users.views.mypage_view', name='mypage'),
    url(r'^mypage/(?P<page_num>(\d+))/$', 'users.views.mypage_view', name='mypage'),

    url(r'^mypage/set/$', 'users.views.mypage_set_view', name='mypage_set'),
    url(r'^mypage/set/(?P<page_num>(\d+))/$', 'users.views.mypage_set_view', name='mypage_set'),

    url(r'^mypage/purchase/$', 'users.views.mypage_purchase_view', name='mypage_purchase'),
    url(r'^mypage/purchase/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_view', name='mypage_purchase'),

    # url(r'^mypage/purchase/$', 'users.views.mypage_purchase_view', name='mypage_purchase'),
    # url(r'^mypage/purchase/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_view', name='mypage_purchase'),
    # url(r'^mypage/purchase/product/$', 'users.views.mypage_purchase_product_view', name='mypage_purchase_product'),
    # url(r'^mypage/purchase/product/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_product_view', name='mypage_purchase_product'),
    # url(r'^mypage/purchase/set/$', 'users.views.mypage_purchase_Fset_view', name='mypage_purchase_set'),
    # url(r'^mypage/purchase/set/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_set_view', name='mypage_purchase_set'),
    # url(r'^mypage/purchase/custom_set/$', 'users.views.mypage_purchase_custom_set_view', name='mypage_purchase_custom_set'),
    # url(r'^mypage/purchase/custom_set/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_custom_set_view', name='mypage_purchase_custom_set'),

    url(r'^mypage/cart/$', 'users.views.mypage_cart_view', name='mypage_cart'),
    url(r'^mypage/cart/json/$', 'users.views.mypage_cart_json_view', name='mypage_cart_json'),
    url(r'^billgate/checksum/$', 'users.views.billgate_payment_checksum', name='billgate_payment_checksum'),


    url(r'^interest/add/$', 'users.views.add_interest', name='add_interest'),
    url(r'^interest/del/$', 'users.views.delete_interest', name='del_interest'),

    url(r'^cart/update/$', 'users.views.update_cart', name='update_cart'),
    url(r'^cart/add/$', 'users.views.add_cart', name='add_cart'),
    url(r'^cart/del/$', 'users.views.delete_cart', name='del_cart'),

    url(r'^purchase/add/$', 'users.views.add_purchase', name='add_purchase'),
    url(r'^purchase/del/$', 'users.views.delete_purchase', name='del_purchase'),

    url(r'^custom/$', 'users.views.make_custom_set', name='make_custom_set'),

#     mobile part

    url(r'^mobile/login_page/$', 'users.views.mobile_login_view', name='mobile_login_page'),

    url(r'^mobile/mypage/$', 'users.views.mobile_mypage_myinfo_view', name='mobile_mypage'),

    url(r'^mobile/mypage/myinfo/$', 'users.views.mobile_mypage_myinfo_view', name='mobile_mypage_myinfo'),

    url(r'^mobile/mypage/set/$', 'users.views.mobile_mypage_set_view', name='mobile_mypage_set'),
    url(r'^mobile/mypage/set/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_set_view', name='mobile_mypage_set'),

    url(r'^mobile/mypage/product/$', 'users.views.mobile_mypage_interesting_view', name='mobile_mypage_product'),
    url(r'^mobile/mypage/product/(?P<page_num>(\d+))/$', 'users.views.mobile_mypage_interesting_view', name='mobile_mypage_product'),

    url(r'^mobile/mypage/purchase/$', 'users.views.mobile_mypage_purchase_list_view', name='mobile_mypage_purchase_list'),

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


    url(r'^mobile/mypage/edit/$', 'users.views.mobile_mypage_myinfo_edit_view', name='mobile_mypage_myinfo_edit'),

    url(r'^mobile/report/$', 'users.views.mobile_report_view', name='mobile_report'),

    url(r'^mobile/report/form/index/$', 'users.views.mobile_report_form_index_view', name='mobile_report_form_index'),

    url(r'^mobile/report/form/$', 'users.views.mobile_report_form_view', name='mobile_report_form'),

    url(r'^mobile/report/detail/(?P<product_id>(\d+))/$', 'users.views.mobile_report_detail_view', name='mobile_report_detail'),

    url(r'^survey/request/$', 'users.views.request_survey', name='request_survey'),

)