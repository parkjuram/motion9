from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    name = models.TextField(null=False)
    email = models.EmailField(null=False)
    sex = models.CharField(max_length=1, null=True)
    age = models.IntegerField(null=True)
    skin_type = models.CharField(max_length=100, null=True)
    skin_color = models.CharField(max_length=10, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)

class Interest(models.Model):
    user = models.ForeignKey('users.UserProfile')
    product = models.ForeignKey('web.Product')
    set = models.ForeignKey('web.Set')
    custom_set = models.ForeignKey('web.CustomSet')
    type = models.CharField(max_length=1, null=False, default='p')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "product"),
            ("user", "set"),
            ("user", "custom_set"))