from ast import Or
from http.client import HTTPResponse
from pickletools import read_uint1
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core import serializers
from customer.models import Customer
from shopowner.models import Order, Product, Shopowner, Shop, Notification

# Create your views here.


def home(request):
    if request.method == "POST":
        scity = request.POST['scity']
        scity = scity.lower()

        sshop = request.POST['sshop']
        sshop = sshop.lower()
        if len(sshop) == 0:
            return redirect('customer:results', scity)
        return redirect('customer:results', scity, sshop)

    if request.session.has_key("customer_email"):
        cust_email = request.session['customer_email']
        cust = Customer.objects.get(email=cust_email)
        return render(request, 'customer/home.html', {
            "cust": cust
        })

    return render(request, "customer/home.html")


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # if customer with this email doesnot exists
        if Customer.objects.filter(email=email).exists():
            cust = Customer.objects.get(email=email)
            # if customer password doesnot matchs
            if password != cust.password:
                error = "password is incorrect"
                return render(request, "customer/login.html", {
                    'error': error
                })
            # success then redirect to home
            # as successful therefore we create session
            request.session['customer_email'] = email
            return HttpResponseRedirect("/")

        else:
            error = "Customer with this email does not exist, You can register yourself first"
            return render(request, "customer/login.html", {
                "error": error,
            })

    return render(request, "customer/login.html")


def register(request):
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # check if customer already exists
        if Customer.objects.filter(email=email).exists():
            error = "Customer with this email already exist"
            return render(request, "customer/register.html", {
                "error": error
            })

        # password check
        if password != cpassword:
            error = "Password dosent match"
            return render(request, "customer/register.html", {
                'error': error
            })
        obj = Customer(email=email, password=password, name=name)
        obj.save()
        request.session['customer_email'] = email
        return redirect('customer:complete_register')
    return render(request, "customer/register.html")


def complete_register(request):
    email = request.session['customer_email']
    cust = Customer.objects.get(email=email)
    if request.method == "POST":
        # now putting all data in customer object
        cust.name = request.POST['name']
        cust.age = request.POST['age']
        cust.contact_number = request.POST['contact_number']
        cust.address = request.POST['address']
        cust.city = request.POST['city']
        cust.state = request.POST['state']
        cust.gender = request.POST['gender']
        try:
            cust.image = request.FILES['image']
        except:
            pass
        cust.save()
        return redirect('/')
    return render(request, 'customer/cmp_registerForm.html', {
        'cust': cust,
        'none': None
    })


def logout(request):
    if request.session.has_key('customer_email'):
        if request.method == "POST":
            del request.session['customer_email']
            return render(request, 'customer/logout.html', {
                'logout': True
            })

        cust_email = request.session['customer_email']
        customer = Customer.objects.get(email=cust_email)
        return render(request, 'customer/logout.html', {
            'cust': customer
        })

    return redirect('customer:home')


def profile(request):
    if not request.session.has_key("customer_email"):
        return redirect('customer:home')

    cust_email = request.session['customer_email']
    customer = Customer.objects.get(email=cust_email)
    return render(request, "customer/profile.html", {
        'cust': customer
    })


def results(request, city_name, shop_name=None):
    try:
        cust_email = request.session['customer_email']
        customer = Customer.objects.get(email=cust_email)
    except:
        customer = None
    if shop_name == None:
        shops = Shop.objects.filter(city=city_name)
    else:
        shops = Shop.objects.filter(city=city_name, name__icontains=shop_name)
    return render(request, "customer/results.html", {
        'shops': shops,
        'cust': customer
    })


def shop_page(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
    except:
        shop = None

    try:
        cust_email = request.session['customer_email']
        customer = Customer.objects.get(email=cust_email)
    except:
        customer = None
    if not shop:
        return render(request, "customer/shop_profile.html", {
            'not_found': True
        })

    product_request_done = None
    if request.method == "POST" and request.POST.get("product_request") == "submit":
        product_name = request.POST['product_name']
        # for making product request user have to login first
        if not request.session.has_key('customer_email'):
            return redirect("customer:login")

        # if logined then we will make request
        cust_email = request.session['customer_email']
        customer = Customer.objects.get(email=cust_email)
        req = "i need " + product_name
        notification = Notification(
            customer=customer, message=req, tag="request", shop=shop)
        notification.save()
        product_request_done = True
    context = {
        'shop': shop,
        'products': shop.products.all()[:4],
        'cust': customer,
        'product_request_done': product_request_done

    }
    return render(request, "customer/shop_profile.html", context=context)


def shop_page_result(request, shop_id):
    product_name = request.GET['product_name']
    try:
        cust_email = request.session['customer_email']
        customer = Customer.objects.get(email=cust_email)
    except:
        customer = None

    shop = Shop.objects.get(id=shop_id)
    products = shop.products.all()
    try:
        # __icontains make search Case insensitive , it also search if some substring is there or not
        product = products.get(
            name__icontains=product_name)
        print(product)
    except:
        product = None

    return render(request, "customer/product_page.html", {
        'product': product,
        'shop': shop,
        'pname': product_name,
        'cust': customer
    })
    return HttpResponse("hi there")


def my_orders(request):
    if not request.session.has_key('customer_email'):
        return redirect('customer:login')
    customer_email = request.session['customer_email']
    customer = Customer.objects.get(email=customer_email)

    order_list = Order.objects.filter(customer=customer)

    return render(request, 'customer/my_orders.html', {
        'cust': customer,
        'order_list': order_list,
    })


def place_order(request, shop_id):
    # print("path is", request.path)
    if not request.session.has_key('customer_email'):
        return redirect('customer:login')
    customer_email = request.session['customer_email']
    customer = Customer.objects.get(email=customer_email)

    if request.method == "POST":
        product_id = request.POST['product_id']
        product = Product.objects.get(id=product_id)
        shop = Shop.objects.get(id=shop_id)
        total_price = request.POST['total_price']
        count = request.POST['count']
        order = Order.objects.create(product=product, shop=shop,
                                     total_price=total_price, count=count, customer=customer)
        order.save()
        return redirect('customer:my_orders')
