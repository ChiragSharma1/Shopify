from django.urls import path
from .views import *

app_name = "shopowner"

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('complete_register', complete_register, name='complete_register'),
    path('profile', profile, name='profile'),
    path('logout', logout, name="logout"),
    path('add_shop', add_shop, name="add_shop"),
    path('my_shop/<int:shopid>/notification/',
         shop_notification, name="shop_notification"),
    path('my_shop/<int:shopid>/product/<int:productid>/',
         edit_product, name="edit_product"),
    path('my_shop/<int:shopid>/', shop_profile, name="my_shop"),
]
