from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    model = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.product_name


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="productimages", null=True)

    def __str__(self):
        return self.product.product_name


class Wishlist(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.products.product_name