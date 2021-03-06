"""
Django settings for Dealme project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

import psycopg2.extensions


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_oiv$f_a$l+f@%gfo!%k6%8-r8fu5y-p+(*m#cyc35%9dylnk='

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
    'storages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'channels',
    'Home',
    'Product',
    'Register',
    'Order',
    'Messenger',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_POST = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'giakinhfullstack@gmail.com'
EMAIL_HOST_PASSWORD = 'giakinh0823'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'Dealme.loginEmail.EmailBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIALACCOUNT_ADAPTER = 'Dealme.myAdapter.MySocialAccountAdapter'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True


SITE = 2

# Use on server when deployment

# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# DEFAULT_HTTP_PROTOCOL = "https"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Dealme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Dealme.wsgi.application'
ASGI_APPLICATION = 'Dealme.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'Dealme',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'GIAKINH',
        'PORT': '',
        'OPTIONS': {
            'unicode_results':True,
            'extra_params': 'ClientCharset=utf8',
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

#
# DATABASES = {
#     "default": {
#         "ENGINE": "djongo",
#         "NAME": "Hara",
#         "CLIENT": {
#             "host": "mongodb+srv://giakinh0823:giakinh0823@mycluster.mlos1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
#             "username": "giakinh0823",
#             "password": "giakinh0823",
#             "authMechanism": "SCRAM-SHA-1",
#         },
#         'LOGGING': {
#             'version': 1,
#             'loggers': {
#                 'djongo': {
#                     'level': 'DEBUG',
#                     'propagate': False,
#                 }
#             },
#         },
#     },
#     'OPTIONS': {
#         'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
#     },
# }

DATABASE_CONNECTION_POOLING = False

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    STATIC_DIR,
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_PUBLIC_KEY = "pk_test_51IooZkD3DR17DTFHglXsWXOIFxEN9A99JTYMKDuXqHygKHHU53fkWCGZ2w4b9gYT2VK9YGJk89K8hUf2rtjApW6C009KexEsg5"
STRIPE_SECRET_KEY = "sk_test_51IooZkD3DR17DTFH37S4K8kSHv0PTc6TIUv3QnupVTiQffGMrpH5TG4L91btdZcF6puRbiYh41Fj6rNv8sRnCb3y00LjEIleGe"
STRIPE_WEBHOOK_SECRET = ""
