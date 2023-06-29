from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api_django/v1/pattern_lib/', include('pattern_lib.urls')),
    path('api_django/v1/pixelation/', include('pixelation.urls')),
    path('api_django/v1/knowledge_library/', include('knowledge_library.urls')),
    path('api_django/ckeditor/', include('ckeditor_uploader.urls')),
    path('api_django/admin/', admin.site.urls),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)