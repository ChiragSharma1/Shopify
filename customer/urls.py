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
    path('shops/<int:shop_id>/result', shop_page_result, name="shop_page_result"),
    path('shops/<int:shop_id>', shop_page, name="shop_page"),
    path('results/<slug:city_name>/<slug:shop_name>', results, name="results"),
    path('results/<slug:city_name>', results, name="results"),
]
