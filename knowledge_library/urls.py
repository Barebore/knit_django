from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ArticleViewSet, CategoryViewSet, MediaViewSet, TermViewSet,
                    TestRichTextViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('articles', ArticleViewSet)
router.register('media', MediaViewSet)
router.register('terms', TermViewSet)
router.register('testrichtext', TestRichTextViewSet)

app_name = 'knowledge_library'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('tinymce/', include('tinymce.urls')),
]