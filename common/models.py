import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# prefix 'N' in class name means renewal version model(2015/01/07)
@python_2_unicode_compatible
class NProduct(models.Model):
    name = models.CharField(max_length=20, null=False)
    brand = models.CharField(max_length=20, null=False, blank=True)
    price = models.IntegerField(null=False, default=0)
    capacity = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class ProductDetail(models.Model):
    product = models.ForeignKey(NProduct, related_name='details')
    function = models.TextField(null=False, blank=True)
    estimation_period = models.SmallIntegerField(null=False, default=0)

    def __str__(self):
        return self.product

@python_2_unicode_compatible
class ProductAnalysis(models.Model):
    product = models.ForeignKey(NProduct, related_name='analysis')
    total_count = models.IntegerField(unique=True, null=False, default=0)
    skin_type = models.CharField(max_length=4, null=False, blank=True)
    feature = models.CharField(max_length=2, null=False, default='no')

    def __str__(self):
        return self.product

@python_2_unicode_compatible
class ProductAnalysisDetail(models.Model):
    product_analysis = models.ForeignKey(ProductAnalysis, related_name='details')
    content = models.TextField(null=False, blank=True)
    count = models.IntegerField(null=False, default=0)
    type = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.product_analysis

    class meta:
        unique_together = (("product_analysis", "content"),)

@python_2_unicode_compatible
class NSurvey(models.Model):
    title = models.CharField(max_length=30, null=False)
    created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class NUserSurvey(models.Model):
    user = models.ForeignKey('auth.User')
    survey = models.ForeignKey(NSurvey)
    comments = models.TextField(null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    def __str__(self):
        return self.comments

@python_2_unicode_compatible
class SurveyResult(models.Model):
    user_survey = models.ForeignKey(NUserSurvey, related_name='survey_result')
    general_review = models.TextField(null=False, blank=True)
    budget_max = models.IntegerField(null=False, default=0)
    budget_min = models.IntegerField(null=False, default=0)
    additional_comment = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.general_review