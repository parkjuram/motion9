from django.conf.urls import patterns, url
from foradmin.views import PurchaseUpdateView, PaymentUpdateView
from supervisor.views import AnalysisView, SupervisorView

urlpatterns = patterns('',
    url(r'^remain_report_count/$', 'common.views.remain_report_count', name='remain_report_count'),
)