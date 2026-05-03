import os
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8!*w7zylcq!!)w2*82jz)u&f0$^dr&n#*rh!yxd5taqzmxx5n='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Render bergan domenni ro'yxatga qo'shamiz
ALLOWED_HOSTS = [
    'my-blog-2-hngy.onrender.com',
    '127.0.0.1',
    'localhost'
]

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


LANGUAGES = [
    ('uz', 'O‘zbekcha'),  
    ('ru', 'Русский'),
    ('en', 'English'),
]

# Tillarni tarjima fayllari saqlanadigan joy
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config.posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'config' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.posts.context_processors.notifications_count',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'my_blog_db',
#         'USER': 'anvar',
#         'PASSWORD': 'Qwerty123$', # O'zingiz o'rnatgan parolni yozing
#         'HOST': '127.0.0.1',
#         'PORT': '5433',
#     }
# }


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'postgresql://anvar:Qwerty123$@127.0.0.1:5433/my_blog_db')
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# Static va Media sozlamalari (fayl oxiriga qo'shing)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'



# Emailni terminalga chiqarish (Test uchun)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tashkent'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "rediss://your-redis-url",
    }
}