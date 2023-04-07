from django.urls import path
from .views import OpenaiAPI

urlpatterns = [
    path('test/', OpenaiAPI.as_view(), name='test'),
]