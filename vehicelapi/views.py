from django.shortcuts import render
from vehicelapi.models import Category,ProductImages,Products,Wishlist
from rest_framework.viewsets import ViewSet,ModelViewSet
from vehicelapi.serializers import CategorySerializer,UserSerializer,ProductSerializer,WishlistSerializer,ImageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions,authentication

class UserView(ViewSet):
    def create(self, request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()

    @action(methods=["POST"],detail=True)
    def add_products(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        category=Category.objects.get(id=id)
        serializer=ProductSerializer(data=request.data,context={"user":request.user,"category":category})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"],detail=True)
    def get_products(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        category=Category.objects.get(id=id)
        pts=category.products_set.all()
        serializer=ProductSerializer(pts,many=True)
        return Response(serializer.data)

class ProductsView(ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list(self, request, *args, **kwargs):
        qs=Products.objects.all()
        serializer=ProductSerializer(qs,many=True)
        return Response(data=serializer.data)
    def retrieve(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        qs=Products.objects.get(id=id)
        serializer=ProductSerializer(qs)
        return Response(data=serializer.data)

    @action(methods=["POST"],detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        prdct=Products.objects.get(id=id)
        serializer=WishlistSerializer(data=request.data,context={"user":request.user,"product":prdct})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/volx/products/{id}/add_images/
    @action(methods=["POST"],detail=True)
    def add_images(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        prdct = Products.objects.get(id=id)
        serializer=ImageSerializer(data=request.data,context={"product":prdct},many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    # localhost:8000/volx/products/{id}/get_images/
    @action(methods=["GET"], detail=True)
    def get_images(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        prdct = Products.objects.filter(id=id)
        images=prdct.productimages_set.all()
        serializer=ImageSerializer(images,many=True)
        return Response(data=serializer.data)


class WishlistView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # localhost:8000/volx/mycart/
    def list(self, request, *args, **kwargs):
        user=request.user
        qs=Wishlist.objects.filter(user=user)
        serializer=WishlistSerializer(qs,many=True)
        return Response(data=serializer.data)
    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        prdct=Wishlist.objects.get(id=id)
        prdct.delete()
        return Response(data="ok")
