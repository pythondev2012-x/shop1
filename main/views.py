from multiprocessing import context

from django.shortcuts import render, redirect
from . import models
from django.contrib.auth import authenticate, login, logout




def index(request):
    categories = models.Category.objects.filter()[:10]
    top_categories = models.Category.objects.filter(is_active=True)[:7]
    products = models.Product.objects.all()

    context = {
        'categories': categories,
        'top_categories':top_categories,
        'products':products
    }
    return render(request, 'front/index.html', context=context)



def product_detail(request, code):
    product = models.Product.objects.get(code=code)

    context = {
        "product":product
    }

    return render(request, 'front/detail.html', context=context)



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