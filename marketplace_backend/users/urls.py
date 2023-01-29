from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter()

router.register('phone', CustomUserViewSet, basename='phone')

urlpatterns = [
    path('api/v1/accounts/', include('allauth.urls')),
    path('api/v1/', include(router.urls))
]
