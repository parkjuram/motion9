from braces.views._access import LoginRequiredMixin, SuperuserRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View
from common_controller.util import helper_get_survey_result_item
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