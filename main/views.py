from multiprocessing import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect
from pip._internal.utils import retry


from . import models
from django.contrib.auth import authenticate, login, logout

from .models import User


def index(request):
    categories = models.Category.objects.filter()[:10]
    top_categories = models.Category.objects.filter(is_active=True)[:7]
    products = models.Product.objects.all()

    context = {
        'categories': categories,
        'top_categories':top_categories,
        'products':products,
    }
    if request.user.is_authenticated:
        wishlist_ids = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)
        context['wishlist_ids'] = wishlist_ids


    return render(request, 'front/index.html', context=context)



def product_detail(request, code):
    product = models.Product.objects.get(code=code)

    context = {
        "product":product
    }

    return render(request, 'front/detail.html', context=context)


def category_filter(request, category_id):
    products = models.Product.objects.filter(category_id=category_id)
    return render(request, 'front/category_filter.html', {'products': products})


# --------------------AUTH------------------------------
def register(request):
    if request.method =="POST":
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            models.User.objects.create_user(username, phone, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

        else:
            return render(request, 'front/register.html')

    return  render(request, 'front/register.html')


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'front/login.html')

def log_out(request):
    logout(request)
    return redirect('index')


def profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.last_name = request.POST.get('last_name')
        user.first_name = request.POST.get('first_name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        if request.FILES.get('photo'):
            user.photo = request.FILES.get('photo')

        user.save()
    return render(request,  'front/profile.html')


@login_required(login_url='login')
def add_wishlist(request, product_code):
    product = models.Product.objects.get(code=product_code)
    element = models.WishList.objects.filter(product=product, user=request.user)
    if not element:
        models.WishList.objects.create(product=product, user=request.user)
    return redirect('index')

@login_required(login_url='login')
def delete_wishlist(request, product_code):
    product = models.Product.objects.get(code=product_code)
    element = models.WishList.objects.filter(product=product, user=request.user)
    if element:
        element.delete()
        return redirect('index')
    return redirect('index')



@login_required(login_url='login')
def wishlist(request):
    wishlist_products = models.WishList.objects.filter(user=request.user)
    context = {
        "wishlist_products":wishlist_products
    }
    return render(request, 'front/wishlist.html', context=context)


@login_required(login_url='login')
def cart(request):
    cart = models.Cart.objects.filter(user=request.user, status=1).first()

    if not cart:
        cart = models.Cart.objects.create(user=request.user, status=1)

    discount_total_price = cart.discount_total_price
    cart_products = models.CartProduct.objects.filter(cart=cart)

    context = {
        "discount_total_price": discount_total_price,
        "cart_products": cart_products,
    }

    return render(request, 'front/cart.html', context=context)


@login_required(login_url='login')
def add_to_cart(request, product_code):
    product = models.Product.objects.get(code=product_code)
    cart = models.Cart.objects.filter(user=request.user, status=1).first()
    if not cart:
        cart =  models.Cart.objects.create(user=request.user, status=1)

    cart_product = models.CartProduct.objects.create(cart=cart, product=product, count=1)
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required(login_url='login')
def cart_product_count_pilus(request, cartproduct_code):
    cart_product = models.CartProduct.objects.get(code=cartproduct_code)
    cart_product.count += 1
    cart_product.save()
    return redirect('cart')



@login_required(login_url='login')
def cart_product_count_minus(request, cartproduct_code):
    cart_product = models.CartProduct.objects.get(code=cartproduct_code)
    if cart_product.count > 1:
        cart_product.count -= 1
        cart_product.save()
    else:
        cart_product.delete()
    return redirect('cart')


@login_required(login_url='login')
def cart_personal(request):
    cart = models.Cart.objects.filter(user=request.user, status=1).first()

    if not cart:
        cart = models.Cart.objects.create(user=request.user, status=1)

    context = {
        'cart': cart
    }

    if request.method == 'POST':
        request.user.username = request.POST['username']
        request.user.address = request.POST['address']
        request.user.phone = request.POST['phone']
        request.user.save()
        return redirect('order')

    return render(request, 'front/cart-personal.html', context=context)


@login_required(login_url='login')
def order(request, cart_code):
    cart = models.Cart.objects.get(code=cart_code)
    cart_products = models.CartProduct.objects.filter(cart=cart)
    for i in cart_products:
        i.product.count -= i.count
        i.product.save()
    cart.status = 2
    cart.save()
    return redirect('thank_you')


def thank_you(request):
    return render(request, 'front/thank-you.html')
