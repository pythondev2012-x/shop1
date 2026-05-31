from django.db import models
from uuid import uuid4

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=150, null= True, blank=True)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='users', null=True, blank=True)


    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"




class Code(models.Model):
    code = models.CharField(max_length=150, unique=True, default=uuid4, blank=True, null=True)


    def __str__(self):
        return self.code

    class Meta:
        abstract = True

class Category(models.Model):
    logo = models.ImageField(upload_to='categories')
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.name



class Product(Code):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Banner(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='banners')
    description = models.TextField()
    product_1 = models.ForeignKey(Product, on_delete=models.SET_NULL , null=True, blank=True)



CART_STATUS = (
    (1, 'No Faol'),
    (2, "Yig'ilmoqda"),
    (3, "Yo'lda"),
    (4, "Yetkazilgan"),
    (5, "Qaytarilgan")
)

class Cart(Code):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CART_STATUS, default=1)
    date = models.DateTimeField(auto_now_add=True)


    @property
    def cart_total_price(self):
        n = 0
        for i in CartProduct.objects.filter(cart=self):
            n += i.total_price
        return n


    @property
    def discount_total_price(self):
        n = 0
        for i in CartProduct.objects.filter(cart=self):
            n += i.discount_price
        return n

    @property
    def count_product(self):
        n = 0
        for i in CartProduct.objects.filter(cart=self):
            n += 1
        return n

    def __str__(self):
        return f'{self.user} - {self.status}'


class CartProduct(Code):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()

    @property
    def total_price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.count
        return self.product.price * self.count

    @property
    def discount_price(self):
        if self.product.discount_price:
            return (self.product.price - self.product.discount_price) * self.count
        return 0

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product}'