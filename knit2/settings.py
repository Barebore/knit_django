"""
Django settings for knit2 project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1ohe+af2^*)ry839^gmwv)s@xhyu_++3l3=$e&w1+vs#ss+hmj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pattern_lib',
    'socks',
    'odin_ass',
    'knowledge_library',
    'sorl.thumbnail',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'ckeditor',
    'tinymce',
    'django_extensions',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # удалить перед диплоем, когда появится статический адресс
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'knit2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'knit2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = Path(BASE_DIR) / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
    'django_filters.rest_framework.DjangoFilterBackend',
    ),
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
} 


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://domain.com",
    "https://api.domain.com",
    "http://localhost:8080",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "http://*",
    "https://*",
]

CORS_ORIGIN_ALLOW_ALL = True # удалить перед диплоем, когда появится статический адресс
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_METHODS = ['*', ]
CORS_ALLOW_HEADERS = ['*', ]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'access-control-allow-origin',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
    'http://localhost',
    'localservername',
    'http://localservername',
    '127.0.0.1',
    u'http://localhost:8888',
    u'http://127.0.0.1:8000',
    u'http://localhost:3000',
]




CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 800,
    },
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 960,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        paste image preview autolink lists link image charmap print preview anchor
        searchreplace visualblocks code fullscreen
        insertdatetime media table paste code help wordcount spellchecker
        advlist autolink lists charmap print hr anchor pagebreak
        searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking
        table emoticons template paste textpattern
    ''',
    'toolbar': '''
        undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify
        | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons
    ''',
    'menubar': 'file edit view insert format tools table help',
    'toolbar1': '''
        undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify
        | bullist numlist outdent indent | link image
    ''',
    'toolbar2': '''
        print preview media | forecolor backcolor emoticons | codesample | 
        charmap anchor | outdent indent | 
    ''',
    'image_advtab': True,
    'file_picker_callback': 'myFilePicker',
    'relative_urls': False,
    'language': 'ru',
}

GRAPH_MODELS ={
'all_applications': True,
'graph_models': True,
}