from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

class UserDetail(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=False)
    balance = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1)
        ]
     )

    def __str__(self):
        return self.user.username

class VendorDetail(models.Model):

    vendor = models.OneToOneField(User,on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=True)
    vendordesc = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.vendor.username

class Item(models.Model):

    vendorName = models.ForeignKey(VendorDetail, on_delete=models.CASCADE)
    itemno = models.UUIDField(default=uuid.uuid4, editable=False)
    itemname = models.CharField(max_length=50, blank=False)
    itemdesc = models.CharField(max_length=200, blank=False)
    itemprice = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
     )
    orders = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
     )
    itemimg = models.ImageField(upload_to='item_images', default='item_images/default.png')

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
     )

class Reviews(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    review = models.CharField(max_length=200, blank=False)

class UserOrders(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    orderdate = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.orderdate = timezone.now()
        self.save()

class WishList(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.OneToOneField(Item,on_delete=models.CASCADE)
