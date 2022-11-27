

from django.urls import path
from vehicelapi.views import UserView,CategoryView,ProductsView,WishlistView
from rest_framework.urlpatterns import include
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("accounts/signup",UserView,basename="signup")
router.register("categories",CategoryView,basename="category")
router.register("products",ProductsView,basename="products")
router.register("wishlist",WishlistView,basename="wishlist")
urlpatterns = [
    path("token/",TokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
]+router.urls