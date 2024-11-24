"""
Django settings for DIY_Dashboard project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lpyv$$@lck621nq$l&i7t8)luq+q@m$u5^%=zi!*5io3c97$zb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'oauth2_provider',

    # Custom apps
    'users',
    'inventory',
    'suppliers',
    'orders',
    'sales',
    'common',
    'warehouse',
]

OAUTH2_PROVIDER = {
    'SCOPES': {
        #users
        'users_create': 'Create users',
        'users_read': 'Read users',
        'users_update': 'Update users',
        'users_delete': 'Delete users',

        #raw materials
        'raw_materials_create': 'Create raw materials',
        'raw_materials_read': 'Read raw materials',
        'raw_materials_update': 'Update raw materials',
        'raw_materials_delete': 'Delete raw materials',

        #finished products
        'finished_products_create': 'Create finished products',
        'finished_products_read': 'Read finished products',
        'finished_products_update': 'Update finished products',
        'finished_products_delete': 'Delete finished products',

        #suppliers
        'suppliers_create': 'Create suppliers',
        'suppliers_read': 'Read suppliers',
        'suppliers_update': 'Update suppliers',
        'suppliers_delete': 'Delete suppliers',

        #purchases orders
        'purchases_orders_create': 'Create purchases orders',
        'purchases_orders_read': 'Read purchases orders',
        'purchases_orders_update': 'Update purchases orders',
        'purchases_orders_delete': 'Delete purchases orders',

        #sales orders
        'sales_orders_create': 'Create sales orders',
        'sales_orders_read': 'Read sales orders',
        'sales_orders_update': 'Update sales orders',
        'sales_orders_delete': 'Delete sales orders',

        #sales bills
        'sales_bills_create': 'Create sales bills',
        'sales_bills_read': 'Read sales bills',
        'sales_bills_update': 'Update sales bills',
        'sales_bills_delete': 'Delete sales bills',

        #purchases bills
        'purchases_bills_create': 'Create purchases bills',
        'purchases_bills_read': 'Read purchases bills',
        'purchases_bills_update': 'Update purchases bills',
        'purchases_bills_delete': 'Delete purchases bills',

        #cart
        'cart_create': 'Create cart',
        'cart_read': 'Read cart',
        'cart_update': 'Update cart',
        'cart_delete': 'Delete cart',

        #favorites
        'favorites_create': 'Create favorites',
        'favorites_read': 'Read favorites',
        'favorites_update': 'Update favorites',
        'favorites_delete': 'Delete favorites',

        #common
        'common_read': 'Read common resources',

        #warehouse
        'warehouse_create': 'Create warehouse items',
        'warehouse_read': 'Read warehouse items',
        'warehouse_update': 'Update warehouse items',
        'warehouse_delete': 'Delete warehouse items',

        # Scopes cho app representatives
        'representatives_create': 'Create representatives',
        'representatives_read': 'Read representatives',
        'representatives_update': 'Update representatives',
        'representatives_delete': 'Delete representatives',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # OAuth2 Authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',    # JWT Authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Chỉ cho phép người dùng đã xác thực
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Token truy cập có hiệu lực trong 60 phút
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Token làm mới có hiệu lực trong 7 ngày
    'ROTATE_REFRESH_TOKENS': True,                  # Tự động thay đổi refresh token sau mỗi lần sử dụng
    'BLACKLIST_AFTER_ROTATION': True,               # Vô hiệu hóa refresh token sau khi được xoay
    'AUTH_HEADER_TYPES': ('Bearer',),               # Loại tiêu đề cho JWT
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DIY_Dashboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DIY_Dashboard.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'diy_company',
        'USER': 'myuser',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
