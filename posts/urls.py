from django.urls import path
from .views import PostViewSet
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")

urlpatterns = [
    path('', include(router.urls)),
]