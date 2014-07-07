from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    phone = models.TextField(null=False, blank=True, default='')
    address = models.TextField(null=False, blank=True, default='')
    sex = models.CharField(max_length=1, null=True)
    age = models.IntegerField(null=True)
    skin_type = models.CharField(max_length=100, null=True)
    skin_color = models.CharField(max_length=10, null=True)
    mileage = models.IntegerField(null=False, default=0)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

signals.post_save.connect(create_user_profile, sender=User)

class Interest(models.Model):
    user = models.ForeignKey('auth.User')
    product = models.ForeignKey('web.Product',null=True)
    set = models.ForeignKey('web.Set',null=True)
    custom_set = models.ForeignKey('users.CustomSet',null=True)
    type = models.CharField(max_length=1, null=False, default='p')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "product"),
            ("user", "set"),
            ("user", "custom_set"))

class Cart(models.Model):
    user = models.ForeignKey('auth.User')
    product = models.ForeignKey('web.Product',null=True)
    set = models.ForeignKey('web.Set',null=True)
    custom_set = models.ForeignKey('users.CustomSet',null=True)
    type = models.CharField(max_length=1, null=False, default='p')
    item_count = models.IntegerField(null=False, default=1)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "product"),
            ("user", "set"),
            ("user", "custom_set"))

class Purchase(models.Model):
    user = models.ForeignKey('auth.User')
    price = models.IntegerField(null=False, default=0)
    address = models.TextField(null=False, blank=True)
    product = models.ForeignKey('web.Product',null=True, blank=True)
    set = models.ForeignKey('web.Set',null=True, blank=True)
    custom_set = models.ForeignKey('users.CustomSet',null=True, blank=True)
    type = models.CharField(max_length=1, null=False, default='p')
    item_count = models.IntegerField(null=False, default=1)
    status = models.CharField(max_length=1, null=False, default='r')
    shipping_number = models.TextField(null=False, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "product"),
            ("user", "set"),
            ("user", "custom_set"))

class CustomSet(models.Model):
    user = models.ForeignKey('auth.User')
    set = models.ForeignKey('web.Set')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "set"))

class CustomSetDetail(models.Model):
    custom_set = models.ForeignKey('users.CustomSet')
    original_product = models.ForeignKey('web.Product', related_name='get_custom_set_detail_from_original_product')
    new_product = models.ForeignKey('web.Product', related_name='get_custom_set_detail_from_new_product')

    class Meta:
        unique_together = (
            ("custom_set", "original_product")
        )