from django.urls import include, path
from rest_framework import routers

from .views import CattegoryViewSet, PatternViewSet

router_v1 = routers.DefaultRouter()

router_v1.register('pattern', PatternViewSet)
router_v1.register('category', CattegoryViewSet)

app_name = 'pattern_lib'

urlpatterns = [
    path('', include(router_v1.urls)),
]
