from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    name = models.TextField(null=False, blank=True, default='')
    phone = models.TextField(null=False, blank=True, default='')
    recent_phone = models.TextField(null=False, blank=True, default='')
    postcode = models.CharField(max_length=10, null=True, blank=True, default='')
    basic_address = models.TextField(null=False, blank=True, default='')
    detail_address = models.TextField(null=False, blank=True, default='')
    sex = models.CharField(max_length=1, null=True, blank=True, default='M')
    age = models.IntegerField(null=True, blank=True)
    skin_type = models.CharField(max_length=100, null=True, blank=True)
    skin_color = models.CharField(max_length=10, null=True, blank=True)
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
    order_id = models.CharField(max_length=64, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "product"),
            ("user", "set"),
            ("user", "custom_set"))

    def __unicode__(self):
        return '[%r]Cart' % (self.id)

class OrderTempInfo(models.Model):
    order_id = models.CharField(max_length=64, null=False, unique=True)
    original_amount = models.CharField(max_length=9, null=True)

class Purchase(models.Model):
    user = models.ForeignKey('auth.User')
    payment = models.ForeignKey('users.Payment', null=True)
    price = models.IntegerField(null=False, default=0)
    product = models.ForeignKey('web.Product',null=True, blank=True)
    set = models.ForeignKey('web.Set',null=True, blank=True)
    custom_set = models.ForeignKey('users.CustomSet',null=True, blank=True)
    type = models.CharField(max_length=1, null=False, default='p')
    item_count = models.IntegerField(null=False, default=1)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    # class Meta:
    #     unique_together = (
    #         ("user", "product"),
    #         ("user", "set"),
    #         ("user", "custom_set"))

class CustomSet(models.Model):
    user = models.ForeignKey('auth.User', related_name='get_custom_sets')
    set = models.ForeignKey('web.Set')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    class Meta:
        unique_together = (
            ("user", "set"))

    def __unicode__(self):
        return '(%r)CustomSet : user(%s) set(%s) is_active(%s)' % (self.id, self.user, self.set, self.is_active)
        # return '(%r)Brand : name_eng(%s) name_kor(%s) is_domestic(%r)' \
        #        % (self.id, self.name_eng, self.name_kor, self.is_domestic)

class CustomSetDetail(models.Model):
    custom_set = models.ForeignKey('users.CustomSet')
    original_product = models.ForeignKey('web.Product', related_name='get_custom_set_detail_from_original_product')
    new_product = models.ForeignKey('web.Product', related_name='get_custom_set_detail_from_new_product')

    class Meta:
        unique_together = (
            ("custom_set", "original_product")
        )

class Payment(models.Model):
    user = models.ForeignKey('auth.User')
    service_id = models.CharField(max_length=20, null=True)
    order_id = models.CharField(max_length=64, null=False, unique=True)
    order_date = models.CharField(max_length=14, null=True)
    transaction_id = models.CharField(max_length=20, null=True)
    auth_amount = models.CharField(max_length=9, null=True)
    auth_date = models.CharField(max_length=14, null=True)
    response_code = models.CharField(max_length=4, null=True)
    response_message = models.TextField(null=False, blank=True, default='')
    detail_response_code = models.CharField(max_length=4, null=True)
    detail_response_message = models.TextField(null=False, blank=True, default='')

    name = models.TextField(null=False, blank=True, default='')
    status = models.CharField(max_length=1, null=True, default='b') # before, ready, ship, finish
    shipping_number = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=False, blank=True, default='')
    postcode = models.CharField(max_length=10, null=True, default='')
    address = models.TextField(null=False, blank=True)
    shipping_requirement = models.TextField(null=False, blank=True)
    mileage = models.IntegerField(null=False, default=0)

    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    def __unicode__(self):
        return '(%r)Payment' % (self.id)


class BeforePayment(models.Model):
    user = models.ForeignKey('auth.User')
    order_id = models.CharField(max_length=64, null=False, unique=True)
    name = models.TextField(null=False, blank=True, default='')
    phone = models.TextField(null=False, blank=True, default='')
    postcode = models.CharField(max_length=10, null=True, default='')
    address = models.TextField(null=False, blank=True)
    shipping_requirement = models.TextField(null=False, blank=True)
    mileage = models.IntegerField(null=False, default=0)

    created = models.DateTimeField(auto_now_add=True, default=datetime.now)

    def __unicode__(self):
        return '(%r)BeforePayment' % (self.id)

class UserSurvey(models.Model):
    user = models.ForeignKey('auth.User')
    survey_item = models.ForeignKey('foradmin.SurveyItem')
    survey_item_option = models.ForeignKey('foradmin.SurveyItemOption')

    class Meta:
        unique_together = ('user', 'survey_item', 'survey_item_option',)

# class SurveyItem(models.Model):
#     question = models.TextField(unique=True)
#     type = models.CharField(max_length=20, null=False, default='radio-vertical')
#
# class SurveyItemOption(models.Model):
#     item = models.ForeignKey('foradmin.SurveyItem', related_name='get_options')
#     content = models.TextField(blank=True)

    # user = models.OneToOneField('auth.User', related_name='profile')