from django.db import models

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

class SurveyItem(models.Model):
    question = models.TextField(unique=True)
    type = models.CharField(max_length=20, null=False, default='radio-vertical')

    def __unicode__(self):
        return '(%r)SurveyItem : question(%s) type(%s)' % (self.id, self.question, self.type)

class SurveyItemOption(models.Model):
    item = models.ForeignKey('foradmin.SurveyItem', related_name='get_options')
    content = models.TextField(blank=True)

    class Meta:
        unique_together = ('item', 'content',)

    def __unicode__(self):
        return '(%r)SurveyItemOption : item(%s) content(%s)' % (self.id, self.item, self.content)