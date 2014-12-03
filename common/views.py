import json
from django.http.response import HttpResponse
from django.shortcuts import render
from users.models import UserSurvey


def remain_report_count(request):
    count = UserSurvey.objects.count()
    return HttpResponse(json.dumps({'count':count}, ensure_ascii=True), content_type="application/json; charset=utf-8")
