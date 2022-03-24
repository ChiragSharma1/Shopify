from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE
from customer.models import Customer
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
    # discount will be in Percentage
    discount = models.FloatField(default="0")

    def __str__(self):
        return self.name + " " + self.details

    @property
    def get_discounted_price(self):
        discount = self.discount
        price = self.price
        discounted_price = price - (discount/100)*price
        return discounted_price


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


class Notification(models.Model):
    message = models.TextField(null=True)
    tag = models.CharField(max_length=50, default="review")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, default="")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.message


class Order(models.Model):
    # tells the product of order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # tells the shop to which order belongs
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)  # customer who order this
    total_price = models.IntegerField(
        default=0)    # total price of this product
    # tells if order is completed or not
    completed = models.BooleanField(default=False)
    count = models.IntegerField(default=1)    # number of products in order

    def __str__(self):
        return f'${self.product.name}-${self.shop.name}'
