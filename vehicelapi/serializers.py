

from rest_framework import serializers
from vehicelapi.models import Category,ProductImages,Products,Wishlist
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    is_active=serializers.CharField(read_only=True)
    class Meta:
        model=Category
        exclude=("date",)

class ImageSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=ProductImages
        fields=["images"]
    def create(self, validated_data):
        product=self.context.get("product")
        return ProductImages.objects.create(**validated_data,product=product)

class ProductSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    category=serializers.CharField(read_only=True)
    product_images=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields="__all__"
    def create(self, validated_data):
        user=self.context.get("user")
        category=self.context.get("category")
        return Products.objects.create(**validated_data,user=user,category=category)

class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)
    class Meta:
        model=Wishlist
        fields="__all__"
    def create(self, validated_data):
        user = self.context.get("user")
        prdct = self.context.get("product")
        return Wishlist.objects.create(**validated_data, user=user, products=prdct)

