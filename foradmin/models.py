from django.db import models

class MainImage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(null=True, upload_to='image/main/')

    def __unicode__(self):
        return '(%r)MainImage : name(%s) image(%r)' % (self.id, self.name, self.image)

class Advertisement(models.Model):
    title = models.CharField(max_length=100, unique=True, default='default')
    type = models.CharField(max_length=20, null=False, blank=True)
    image = models.ImageField(null=True, upload_to='image/advertisement/')
    link = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '(%r)Advertisement : image(%s) link(%r)' % (self.id, self.image, self.link)

class Preference(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '(%r)Preference : name(%s) content(%r)' % (self.id, self.name, self.content)