# -*- coding:utf-8 -*-
from braces.views._access import LoginRequiredMixin, SuperuserRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from common.models import NProduct
from common_controller.analysis.analysis_blog_review import AnalysisBlogReview
from common_controller.analysis.blog_review_link_scrapper import BlogReviewLinkScrapper
from common_controller.util import helper_get_survey_result_item, http_response_by_json
from users.models import UserSurvey


class SupervisorView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request,
                      "supervisor/index.html",
            {},
        )

class AnalysisView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_survey = UserSurvey.objects.order_by('id').all()
        analysis_list = []
        for item in user_survey:
            analysis_ = {
                'id': item.id,
                'username': item.user.profile.name,
                'email': item.user.email,
                'sex': item.user.profile.sex,
                'age':item.user.profile.age,
                'result_file_name': item.result_file_name,
                'question':[],
                'comments': item.comments,
                'created': item.created
            }
            for detail_item in item.get_survey_detail.all():
                analysis_['question'].append({
                    'title': detail_item.survey_item_option.item.question,
                    'answer': detail_item.survey_item_option.content
                })

            analysis_list.append(analysis_)

        return render(request,
                      "supervisor/analysis.html",
                      {'analysis_list': analysis_list} )

    def post(self, request, *args, **kwargs):
        ids = request.POST.get('ids')
        ids = ids.split("@")
        values = request.POST.get('values')
        values = values.split("@")

        for i in range(len(ids)):
            id = ids[i]
            value = values[i]
            UserSurvey.objects.filter(id=id).update(result_file_name=str(value))

        return redirect("supervisor:analysis")

class ProductAnalysisView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        products = NProduct.objects.values()
        return render(request,
                      "supervisor/product_analysis.html",
                      {'products': products} )


    def post(self, request, *args, **kwargs):
        querys = request.POST.get('queryConcatString').split("@");
        querys = map(lambda x:'"'+x+'"', querys)
        querys = map(lambda x:x.encode('utf-8'), querys)
        blog_review_link_scrapper = BlogReviewLinkScrapper()
        blog_url_list = blog_review_link_scrapper.startScrapping(query_item_list = querys)
        analysis_blog_review = AnalysisBlogReview()
        analysis_result_list = analysis_blog_review.startAnalysis(blog_url_list)
        return http_response_by_json(None, {'analysis_result_list':analysis_result_list} )

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ProductAnalysisView, self).dispatch(*args, **kwargs)