from django.urls import include, path
from rest_framework import routers
from .views import PatternViewSet, CattegoryViewSet, image_process, multi_part

router_v1 = routers.DefaultRouter()

router_v1.register('pattern', PatternViewSet)
router_v1.register('category', CattegoryViewSet)

app_name = 'pattern_lib'

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('image_process/', image_process, name='image_process'),
    path('multi_part/', multi_part, name='multi_part'),
]
