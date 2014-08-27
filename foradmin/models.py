from django.db import models

class MainImage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(null=True, upload_to='image/main/')

    def __unicode__(self):
        return '(%r)MainImage : name(%s) is_set(%r)' % (self.id, self.name, self.image)

class Advertisement(models.Model):
    image = models.ImageField(null=True, upload_to='image/advertisement/')
    type = models.CharField(null=False, blank=True)
    link = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '(%r)Advertisement : image(%s) link(%r)' % (self.id, self.image, self.link)

