from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Category, Pattern
from .serializers import (CategorySerializer, PatternDetailSerializer,
                          PatternSerializer)


class PatternViewSet(viewsets.ModelViewSet):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    # pagination_class = None
    filterset_fields = ('category', )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = LimitOffsetPagination

    # для обработки запроса формата pattern/3, где 3 - id поста
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PatternDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class CattegoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = ()

