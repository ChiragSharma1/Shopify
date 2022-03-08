from django.urls import path
from .views import *

app_name = "customer"
urlpatterns = [
    path('', home, name="home"),
    path('login', login, name="login"),
    path('register', register, name="register"),
    path('cmp_register', complete_register, name="complete_register"),
    path('logout', logout, name="logout"),
    path('profile', profile, name="profile"),
    path('myorders', my_orders, name="my_orders"),
    path('shops/<int:shop_id>/result', shop_page_result, name="shop_page_result"),
    path('shops/<int:shop_id>/order', place_order, name='place_order'),
    path('shops/<int:shop_id>', shop_page, name="shop_page"),
    path('results/search', results, name="results"),
]
