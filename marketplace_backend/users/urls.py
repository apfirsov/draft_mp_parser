from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter()

router.register('phone', CustomUserViewSet, basename='phone')

urlpatterns = [
    path('', include(router.urls))]