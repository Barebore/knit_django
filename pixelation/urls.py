from django.urls import include, path
from rest_framework import routers

from .views import create_image, image_process, multi_part

app_name = 'pixelation'

urlpatterns = [
    path('image_process/', image_process, name='image_process'),
    path('multi_part/', multi_part, name='multi_part'),
    path('create_image/', create_image, name='create_image'),
]
