from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE
# Create your models here.


class Shopowner(models.Model):

    user = models.OneToOneField(User, on_delete=CASCADE)
    age = models.IntegerField(validators=[MinValueValidator(18)], null=True)
    profile_complete = models.BooleanField(default=False)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    image = models.ImageField(
        upload_to="shopowner/images", default="shopowner/images/shopowner_default.jpg")

    def name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return self.name()


class Product(models.Model):
    name = models.CharField(max_length=40)
    details = models.CharField(max_length=150)
    price = models.IntegerField()
    image = models.ImageField(
        upload_to="product/images", default="product/images/product_default.jpg")
    # this will be measuring unit
    unit = models.CharField(max_length=50, default="Kg")

    def __str__(self):
        return self.name + " " + self.details


class Shop(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    shopowner = models.ForeignKey(
        Shopowner, on_delete=models.CASCADE, default="", related_name='shop')
    products = models.ManyToManyField(Product, related_name='shop')
    image = models.ImageField(upload_to="shop/images",
                              default="shop/images/shop_default.jpg")

    def __str__(self):
        return self.name
