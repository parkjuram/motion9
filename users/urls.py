from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^registration/$', 'users.views.registration', name='registration'),
    url(r'^registration_page/$', 'users.views.registration_view', name='registration_page'),
    url(r'^login/$', 'users.views.login', name='login'),
    url(r'^login_page/$', 'users.views.login_view', name='login_page'),
    url(r'^logout/$', 'users.views.logout_', name='logout'),
    url(r'^update/$', 'users.views.update', name='update'),

    url(r'^mypage/$', 'users.views.mypage_view', name='mypage'),
    url(r'^mypage/(?P<page_num>(\d+))/$', 'users.views.mypage_view', name='mypage'),

    url(r'^mypage/set/$', 'users.views.mypage_set_view', name='mypage_set'),
    url(r'^mypage/set/(?P<page_num>(\d+))/$', 'users.views.mypage_set_view', name='mypage_set'),

    url(r'^mypage/cart/$', 'users.views.mypage_cart_view', name='mypage_cart'),

    url(r'^mypage/purchase/product/$', 'users.views.mypage_purchase_product_view', name='mypage_purchase_product'),
    url(r'^mypage/purchase/product/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_product_view', name='mypage_purchase_product'),

    url(r'^mypage/purchase/set/$', 'users.views.mypage_purchase_set_view', name='mypage_purchase_set'),
    url(r'^mypage/purchase/set/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_set_view', name='mypage_purchase_set'),

    url(r'^mypage/purchase/custom_set/$', 'users.views.mypage_purchase_custom_set_view', name='mypage_purchase_custom_set'),
    url(r'^mypage/purchase/custom_set/(?P<page_num>(\d+))/$', 'users.views.mypage_purchase_custom_set_view', name='mypage_purchase_custom_set'),

    url(r'^interest/add/$', 'users.views.add_interest', name='add_interest'),
    url(r'^interest/del/$', 'users.views.delete_interest', name='del_interest'),

    url(r'^cart/add/$', 'users.views.add_cart', name='add_cart'),
    url(r'^cart/del/$', 'users.views.delete_cart', name='del_cart'),

    url(r'^purchase/add/$', 'users.views.add_purchase', name='add_purchase'),
    url(r'^purchase/del/$', 'users.views.delete_purchase', name='del_purchase'),
    # @app.route('/interest/add', methods = ['POST'])



# @app.route('/mypage/set', methods = ['GET'])
# @app.route('/mypage/set/<int:pageNum>', methods = ['GET'])
# @login_required
# def myPageSetWeb(pageNum=None):

)