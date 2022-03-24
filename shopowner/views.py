from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .models import Notification, Product, Shop, Shopowner
# Create your views here.


def home(request):
    if not request.user.is_authenticated or not hasattr(request.user, "shopowner"):
        return redirect('shopowner:login')
    if hasattr(request.user, "shopowner"):
        return render(request, "shopowner/home.html", {
            'user': request.user,
            'shops': request.user.shopowner.shop.all()
        })
    return render(request, 'shopowner/home.html', {
        'user': request.user
    })


def login(request):

    if request.user.is_authenticated and hasattr(request.user, "shopowner"):
        return redirect('shopowner:home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            usr = User.objects.get(email=email)
            if hasattr(usr, "shopowner"):
                if password != usr.password:
                    error = "Incorrect Password"
                    return render(request, 'shopowner/login.html', {
                        'user': None,
                        'error': error
                    })
                auth_login(request, usr)
                return redirect('shopowner:home')
            else:
                error = "User with this email does not exist"
                return render(request, "shopowner/login.html", {
                    'error': error,
                    'user': None
                })
        else:
            error = "User with this email does not exist"
            return render(request, 'shopowner/login.html', {
                'error': error,
                'user': None
            })

    return render(request, 'shopowner/login.html', {
        'user': None
    })


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            error = "User with username already exists, use some differet username"
            return render(request, 'shopowner/register.html', {
                'user': None,
                'error': error
            })
        if User.objects.filter(email=email).exists():
            error = "User with this email already exists"
            return render(request, 'shopowner/register.html', {
                'user': None,
                'error': error
            })
        password = request.POST['password']
        con_password = request.POST['con_password']

        if password != con_password:
            error = "Password does not match"
            return render(request, 'shopowner/register.html', {
                'error': error,
                'user': None
            })
        u = User(username=username, email=email,
                 password=password, first_name=first_name, last_name=last_name)

        u.save()
        auth_login(request, u)
        owner = Shopowner(user=u)
        owner.save()
        return redirect('shopowner:complete_register')
    return render(request, 'shopowner/register.html', {
        'user': None
    })


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('shopowner:home')
    return render(request, 'shopowner/logout.html')


def profile(request):
    pass


def complete_register(request):
    user = request.user
    if request.method == "POST":
        owner = user.shopowner
        owner.age = request.POST['age']
        owner.address = request.POST['address']
        owner.city = request.POST['city']
        owner.state = request.POST['state']
        try:
            img = request.FILES['image']
        except:
            img = None

        if img:
            owner.image = img
        owner.profile_complete = True
        owner.save()
        return redirect('shopowner:home')
    return render(request, 'shopowner/complete_register.html', {
        'user': user
    })


@login_required(login_url="/partner_with_us/login")
def add_shop(request):
    if not hasattr(request.user, "shopowner"):
        return redirect('shopowner:login')
    if request.method == "POST":
        user = request.user
        shopowner = Shopowner.objects.get(user=user)
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        shop = Shop(name=name, address=address, city=city,
                    state=state, shopowner=shopowner)

        # now getting image
        try:
            img = request.FILES['image']
        except:
            img = None
        if img:
            shop.image = img
        shop.save()
        return redirect('shopowner:home')
    return render(request, 'shopowner/add_shop.html', {
        'user': request.user
    })


@login_required(login_url="/partner_with_us/login")
def shop_profile(request, shopid):

    usr = request.user
    shops = usr.shopowner.shop.all()
    try:
        s = shops.get(id=shopid)
    except:
        s = None

    if s and request.method == "POST":  # add products to this shop
        name = request.POST['name']
        details = request.POST['detail']
        price = request.POST['price']
        unit = request.POST['unit']
        discount = request.POST['discount']
        product = Product(name=name, details=details,
                          price=price, unit=unit, discount=discount)
        try:
            image = request.FILES['image']
        except:
            image = None
        if image:
            product.image = image
        product.save()
        s.products.add(product)
        s.save()
        return redirect('shopowner:my_shop', s.id)

    return render(request, "shopowner/shop_profile.html", {
        'user': request.user,
        'shop': s,
        'products': s.products.all()[:5]
    })


@login_required(login_url="partner_with_us/login")
def shop_notification(request, shopid):
    s = Shop.objects.get(id=shopid)
    notification = Notification.objects.filter(shop=s)
    notifications_count = notification.count()
    return render(request, "shopowner/shop_notification.html", {
        'user': request.user,
        'shop': s,
        'notifications': notification,
        'notifications_count': notifications_count,
    })


@login_required(login_url='partner_with_us/login')
def edit_product(request, shopid, productid):
    shop = Shop.objects.filter(id=shopid).first()
    product = Product.objects.filter(id=productid).first()
    if request.method == "POST":
        product.name = request.POST['name']
        product.details = request.POST['details']
        product.price = request.POST['price']
        product.unit = request.POST['unit']
        product.discount = request.POST['discount']
        try:
            product.image = request.FILES['image']
        except:
            pass
        product.save()
        return redirect('shopowner:my_shop', shopid)
    return render(request, 'shopowner/shop_edit_product.html', {
        'product': product,
        'user': request.user,
        'shop': shop})
