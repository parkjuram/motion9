# -*- coding:utf-8 -*-
from braces.views._access import LoginRequiredMixin, SuperuserRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View, TemplateView
from common.models import NProduct, ProductAnalysis, ProductAnalysisDetail
from common_controller.analysis.analysis_blog_review import AnalysisBlogReview
from common_controller.analysis.blog_review_link_scrapper import BlogReviewLinkScrapper
from common_controller.util import helper_get_survey_result_item, http_response_by_json, convert_skintype_key_to_value, \
    convert_feature_key_to_value
from supervisor.tasks import analysis_product
from users.models import UserSurvey, SurveyResult, SurveyResultDetail
import json
from web.models import Category

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
            for detail_item in item.details.all():
                analysis_['question'].append({
                    'title': detail_item.survey_item_option.survey_item.question,
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
        if ( request.POST.has_key('queryConcatString') ):
            querys = request.POST.get('queryConcatString').split("@");
            querys = map(lambda x:'"'+x+'"', querys)
            querys = map(lambda x:x.encode('utf-8'), querys)
            task = analysis_product.apply_async(args=[querys])
            response = HttpResponse({}, status=202)
            response['Location'] = reverse('supervisor:analysis_status', kwargs={'task_id':task.id})
            return response
        else:
            product_id = request.POST.get('product_id')
            total_count = request.POST.get('total_count')
            skin_type = request.POST.get('skin_type')
            feature = request.POST.get('feature')
            analysis_detail_list = json.loads(request.POST.get('analysis_detail_list'))

            product_analysis, created = ProductAnalysis.objects.get_or_create(product_id=product_id,
                                                                              defaults={ 'total_count': total_count,
                                                                                         'skin_type': skin_type,
                                                                                         'feature': feature })

            if not(created):
                product_analysis.total_count= total_count
                product_analysis.skin_type= skin_type
                product_analysis.feature= feature
                product_analysis.save()

            for analysis_detail_item in analysis_detail_list:
                product_analysis_detail, created = ProductAnalysisDetail.objects.get_or_create(product_analysis_id=product_analysis.id, content=analysis_detail_item['keyword'],
                                                           defaults={ 'count': analysis_detail_item['count'],
                                                                      'type': analysis_detail_item['type'] })

                if not(created):
                    product_analysis_detail.count= analysis_detail_item['count']
                    product_analysis_detail.type= analysis_detail_item['type']
                    product_analysis_detail.save()

            return http_response_by_json(None)

class UserSurveyListView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_surveys = UserSurvey.objects.select_related('user').order_by('-created').all()
        user_surveys_ = []
        for user_survey in user_surveys:
            user_survey_ = {
                'id': user_survey.id,
                'username': user_survey.user.profile.name,
                'email': user_survey.user.email,
                'survey_enter_date': user_survey.created,
                'is_entered': False,
                'entered_date': '',
                'is_again': hasattr(user_survey,'usersurveyagain')
            }
            if user_survey.results.exists():
                survey_result = user_survey.results.first()
                user_survey_.update( {
                    'is_entered': True,
                    'entered_date': survey_result.created
                })

            user_surveys_.append(user_survey_)


        return render(request,
                      "supervisor/user_survey_list.html",
                      {'user_surveys': user_surveys_} )

    def post(self, request, *args, **kwargs):
        pass

class CreateOrUpdateSurveyResultView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_survey_id = self.kwargs['user_survey_id']
        user_survey = UserSurvey.objects.get(id=user_survey_id)
        user_survey_detail_list = user_survey.details.all()
        user_survey_details = []
        for user_survey_detail in user_survey_detail_list:
            question = user_survey_detail.survey_item_option.survey_item.question
            answer = user_survey_detail.survey_item_option.content
            user_survey_details.append( {
                'question': question,
                'answer': answer
            })


        products_ = []
        products = NProduct.objects.all()
        brands = NProduct.objects.distinct('brand').values_list('brand', flat=True)
        categories = Category.objects.values_list('name', flat=True)

        for product in products:
            product_ = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'brand': product.brand,
                'category': product.category,
                'thumbnail': product.thumbnail,
                'skin_type': "",
                'feature': "",
                'keyword': []
            }
            name = product.name
            price = product.price
            brand = product.brand
            category = product.category.name
            if product.analysis.exists():
                product_analysis = product.analysis.first()
                product_.update({
                    'skin_type': convert_skintype_key_to_value(product_analysis.skin_type),
                    'feature': convert_feature_key_to_value(product_analysis.feature)
                })
                if product_analysis.details.exists():
                    product_analysis_details = product_analysis.details.all()
                    for product_analysis_detail in product_analysis_details:
                        product_['keyword'].append(product_analysis_detail.content)

            products_.append(product_)

        rendering_params = {'user_survey_id': user_survey_id,
                            'user_survey_again': user_survey.usersurveyagain if hasattr(user_survey,'usersurveyagain') else False,
                            'user_survey_details': user_survey_details,
                            'brands': brands,
                            'categories': categories,
                            'products': products_}

        if user_survey.results.exists():
            survey_result = user_survey.results.first()
            rendering_params.update({
                'general_review': survey_result.general_review,
                'budget_max': survey_result.budget_max,
                'budget_min': survey_result.budget_min,
                'additional_comment': survey_result.additional_comment
            })

        return render(request,
                      "supervisor/create_or_update_survey_result.html",
                      rendering_params )

    def post(self, request, *args, **kwargs):
        user_survey_id = self.kwargs['user_survey_id']

        general_review = request.POST.get('general_review')
        budget_min = request.POST.get('budget_min')
        budget_max = request.POST.get('budget_max')
        additional_comment = request.POST.get('additional_comment')
        selected_product_list = json.loads(request.POST.get('selected_product_list'))

        survey_result, created = SurveyResult.objects.get_or_create(user_survey_id=user_survey_id,
                                                                          defaults={ 'general_review': general_review,
                                                                                     'budget_max': budget_max,
                                                                                     'budget_min': budget_min,
                                                                                     'additional_comment': additional_comment })

        if not(created):
            survey_result.general_review= general_review
            survey_result.budget_max= budget_max
            survey_result.budget_min= budget_min
            survey_result.additional_comment= additional_comment
            survey_result.save()

        SurveyResultDetail.objects.filter(survey_result_id=survey_result.id).delete()
        for selected_product in selected_product_list:
            product_analysis_detail, created = SurveyResultDetail.objects.get_or_create(survey_result_id=survey_result.id,
                                                                                        product_id=selected_product['product-id'])


        return http_response_by_json(None)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CreateOrUpdateSurveyResultView, self).dispatch(*args, **kwargs)

class CheckImageSizeView(SuperuserRequiredMixin, TemplateView):
    template_name = "supervisor/check_image_size.html"

    def get_context_data(self, **kwargs):
        context = super(CheckImageSizeView, self).get_context_data(**kwargs)

        context['products'] = NProduct.objects.all()

        return context


def analysis_status(request, task_id):
    task = analysis_product.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return http_response_by_json(None, response)