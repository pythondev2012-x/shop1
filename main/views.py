from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models


def index(request):
    categories = models.Category.objects.filter()[:10]
    top_categories = models.Category.objects.filter(is_active=True)[:7]
    products = models.Product.objects.all()
    context = {
        'categories': categories,
        'top_categories': top_categories,
        'products': products
    }
    return render(request, 'front/index.html', context=context)


def product_detail(request, code):
    product = models.Product.objects.get(code=code)
    context = {
        "product": product
    }
    return render(request, 'front/detail.html', context=context)


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if models.User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band! Boshqa username tanlang.")
            return render(request, 'front/register.html')

        if password == confirm_password:
            models.User.objects.create_user(username, phone, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Parollar mos kelmadi!")
            return render(request, 'front/register.html')
    return render(request, 'front/register.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
            return render(request, 'front/login.html')
    return render(request, 'front/login.html')


def logout_page(request):
    logout(request)
    return redirect('index')