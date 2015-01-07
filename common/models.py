from django.db import models

# prefix 'N' in class name means renewal version model(2015/01/07)

class NProduct(models.Model):
    name = models.CharField(max_length=20, null=False)
    brand = models.CharField(max_length=20, null=False, blank=True)
    price = models.IntegerField(null=False, default=0)
    capacity = models.IntegerField(null=False, default=0)

class ProductDetail(models.Model):
    product = models.ForeignKey(NProduct, related_name='details')
    function = models.TextField(null=False, blank=True)
    estimation_period = models.SmallIntegerField(null=False, default=0)