from django.conf.urls import patterns, url
from web.views import SurveyResultView, SurveyResultDetailView

urlpatterns = patterns('',
                       url(r'^test/$', 'web.views.test_view', name='test'),

                       url(r'^payment/before/$', 'web.views.before_payment', name='before_payment'),

                       # url(r'^payment/pay_explorer/$', 'web.views.payment_pay_explore_view', name='payment_pay_explore'),
                       url(r'^payment/return/$', 'web.views.payment_return_view', name='payment_return'),
                       url(r'^payment/return_mobile_web/$', 'web.views.payment_return_mobile_web_view',
                           name='payment_return_mobile_web'),

                       url(r'^payment/complete/$', 'web.views.payment_complete_view', name='payment_complete'),
                       url(r'^payment/complete/(?P<payment_id>(\d+))/$', 'web.views.payment_complete_view',
                           name='payment_complete'),

                       # url(r'^payment/pay_chrome/$', 'web.views.payment_pay_chrome_view', name='payment_pay_chrome'),
                       # url(r'^payment/return_chrome/$', 'web.views.payment_return_chrome_view', name='payment_return_chrome'),
                       url(r'^$', 'web.views.index_view', name='index'),
                       url(r'^index/$', 'web.views.index_view', name='index'),

                       url(r'^shop/product/$', 'web.views.shop_product_view', name='shop_product'),
                       url(r'^shop/product/(?P<category_id>(\d+))/$', 'web.views.shop_product_view',
                           name='shop_product'),
                       url(r'^shop/product/page/(?P<page_num>(\d+))/$', 'web.views.shop_product_view',
                           name='shop_product'),
                       url(r'^shop/product/(?P<category_id>(\d+))/page/(?P<page_num>(\d+))/$',
                           'web.views.shop_product_view', name='shop_product'),

                       url(r'^product/(?P<product_id>(\d+))/$', 'web.views.product_view', name='product'),
                       url(r'^product/(?P<product_id>(\d+))/json/$', 'web.views.product_json_view',
                           name='product_json'),
                       url(r'^product/(?P<product_id>(\d+))/modal/$', 'web.views.product_modal_view',
                           name='product_modal'),

                       url(r'^shop/set/$', 'web.views.shop_set_view', name='shop_set'),
                       url(r'^shop/set/(?P<category_id>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
                       url(r'^shop/set/page/(?P<page_num>(\d+))/$', 'web.views.shop_set_view', name='shop_set'),
                       url(r'^shop/set/(?P<category_id>(\d+))/page/(?P<page_num>(\d+))/$', 'web.views.shop_set_view',
                           name='shop_set'),

                       url(r'^set/(?P<set_id>(\d+))/$', 'web.views.set_view', name='set'),

                       url(r'^customize/set/make/(?P<set_id>(\d+))/$', 'web.views.customize_set_make_view',
                           name='customize_set_make'),
                       url(r'^customize/set/$', 'web.views.customize_set_view', name='customize_set'),
                       url(r'^customize/set/(?P<set_id>(\d+))/$', 'web.views.customize_set_detail_view',
                           name='customize_set_detail'),
                       url(r'^customize/set/save/$', 'web.views.customize_set_save_view', name='customize_set_save'),

                       url(r'^help/faq/$', 'web.views.help_faq_view', name='help_faq'),

                       url(r'^report/$', 'web.views.report_view', name='report'),

                       url(r'^report/detail/(?P<product_id>(\d+))/$', 'web.views.report_detail_view',
                           name='report_detail'),

                       url(r'^report/detail/(?P<product_id>(\d+))/mbodal/$', 'web.views.report_detail_modal_view',
                           name='report_detail_modal'),

                       url(r'^report/form/$', 'web.views.report_form_view', name='report_form'),

                       url(r'^report/form/index/$', 'web.views.report_form_index_view', name='report_form_index'),

                       url(r'^survey/list/json', 'web.views.survey_list_in_json', name='survey_list_in_json'),

                       url(r'^survey/detail/$', 'web.views.survey_detail_view', name='survey_detail'),

                       url(r'^survey/(?P<pk>(\d+))/$', 'web.views.survey_result_view', name='survey_result'),

                       url(
                           regex=r'^survey2/(?P<pk>(\d+))/$',
                           view=SurveyResultView.as_view(),
                           name='survey2_result'
                       ),

                       url(
                           regex=r'^survey2/(?P<pk>(\d+))/(?P<product_type>(\w+))$',
                           view=SurveyResultDetailView.as_view(),
                           name='survey2_result_detail'
                       ),

                       url(r'^chart/$', 'web.views.chart_view', name='chart'),

                       )