from ast import Or
from django.contrib import admin
from .models import Product, Shop, Shopowner, Notification, Order
# Register your models here.

admin.site.register(Shopowner)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Notification)
admin.site.register(Order)
