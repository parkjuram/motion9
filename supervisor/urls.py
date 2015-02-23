from django.conf.urls import patterns, url
from foradmin.views import PurchaseUpdateView, PaymentUpdateView
from supervisor.views import AnalysisView, SupervisorView, ProductAnalysisView, UserSurveyListView, \
    CreateOrUpdateSurveyResultView, CheckImageSizeView

urlpatterns = patterns('',

    url(
        regex=r'^$',
        view=SupervisorView.as_view(),
        name='index'
    ),
    url(
        regex=r'^analysis/$',
        view=AnalysisView.as_view(),
        name='analysis'
    ),
    url(r'^analysis/product/status/(?P<task_id>([\w-]+))/$', 'supervisor.views.analysis_status', name='analysis_status'),
    url(
        regex=r'^analysis/product/$',
        view=ProductAnalysisView.as_view(),
        name='analysis_product'
    ),
    url(
        regex=r'^user-survey/$',
        view=UserSurveyListView.as_view(),
        name='user_survey_list'
    ),
    url(
        regex=r'^user-survey/(?P<user_survey_id>(\d+))/$',
        view=CreateOrUpdateSurveyResultView.as_view(),
        name='create_or_update_survey_result'
    ),
    url(
        regex=r'^check-image-size/$',
        view=CheckImageSizeView.as_view(),
        name='check_image_size'
    ),





    # url(r'^manage/shipping/$', 'foradmin.views.manage_shipping_view', name='manage_shipping'),
    # # url(r'^manage/purchase/update/(?P<pk>\d+)/$', 'foradmin.views.purchase_update', name='purchase_update'),
    # url(r'^manage/payment/update/$', 'foradmin.views.payment_update', name='payment_update'),
    # url(r'^manage/payment/update/(?P<pk>\d+)/$', 'foradmin.views.payment_update', name='payment_update'),
    #
    # url(
    #     regex=r'^function/purchase/update/(?P<pk>\d+)/$',
    #     view=PurchaseUpdateView.as_view(),
    #     name='function_purchase_update'
    # ),
    # url(
    #     regex=r'^function/payment/update/(?P<pk>\d+)/$',
    #     view=PaymentUpdateView.as_view(),
    #     name='function_payment_update'
    # ),
)