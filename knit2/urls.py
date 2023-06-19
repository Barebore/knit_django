from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('pattern_lib/', include('pattern_lib.urls')),
    path('knowledge_library/', include('knowledge_library.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)