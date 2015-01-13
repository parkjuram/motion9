from datetime import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class MainImage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(null=True, upload_to='image/main/')

    def __unicode__(self):
        return '(%r)MainImage : name(%s) image(%r)' % (self.id, self.name, self.image)

class Advertisement(models.Model):
    title = models.CharField(max_length=100, unique=True, default='default')
    category = models.ForeignKey('web.Category',null=True)
    image = models.ImageField(null=True, upload_to='image/advertisement/')
    mobile_image = models.ImageField(null=True, upload_to='image/advertisement/mobile/')

    def __unicode__(self):
        return '(%r)Advertisement : image(%r)' % (self.id, self.image)

class Preference(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '(%r)Preference : name(%s) content(%r)' % (self.id, self.name, self.content)

@python_2_unicode_compatible
class Survey(models.Model):
    title = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class SurveyItem(models.Model):
    survey = models.ForeignKey('foradmin.Survey')
    question = models.TextField()
    type = models.CharField(max_length=20, null=False, default='radio-vertical')
    order = models.IntegerField(null=False, default=0)

    class Meta:
        unique_together = (("survey", "question"),)

    def __str__(self):
        return '%r - SurveyItem : item[%r] question[%s] type[%s]' % (self.id, self.item, self.question, self.type)

@python_2_unicode_compatible
class SurveyItemOption(models.Model):
    survey_item = models.ForeignKey('foradmin.SurveyItem')
    content = models.TextField(null=False, blank=True)
    order = models.IntegerField(null=False, default=0)

    class Meta:
        unique_together = ('survey_item', 'content',)

    def __str__(self):
        return '%r - SurveyItemOption : item[%s] content[%s] order[%r]' % (self.id, self.item.question, self.content, self.order)