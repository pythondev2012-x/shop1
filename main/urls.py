from django.urls import path
from . import  views
urlpatterns = [
    path('',views.index,name='index'),
    path('product-detail/<str:code>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
]