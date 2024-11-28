"""
Django settings for DIY_Dashboard project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from decouple import config
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
from firebase_admin import credentials
import firebase_admin

load_dotenv()

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET') 
})

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lpyv$$@lck621nq$l&i7t8)luq+q@m$u5^%=zi!*5io3c97$zb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.vercel.app', 'localhost', '54.224.77.45', '127.0.0.1']



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
    'drf_yasg',

    # Custom apps
    'users',
    'inventory',
    'suppliers',
    'orders',
    'sales',
    'common',
    'warehouse',
    'payment',
]

DEFAULT_CLIENT_ID = "KD4eWL1NsMJR2ovQKjdVCBwy17CE5bqimmUywX5q"
DEFAULT_CLIENT_SECRET = "dzVHEAouKvZtqoGOIjwiZB7imFqWq48t98HA35upscEkYVYKPNbSlpFHEJKKOuuSgkieoJ0N0IutOUwCHBHhgYCRWNeAyxMxof44vQuVexs8a2pVYKeDOYzU2CZ4GAWT"

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')
FIREBASE_APP_ID = os.getenv('FIREBASE_APP_ID')


OAUTH2_PROVIDER = {
    'OAUTH2_VALIDATOR_CLASS': 'users.validators.CustomOAuth2Validator',
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

        #enduser
        'enduser' : 'all permission in enduser',

        # #cart
        # 'cart_create': 'Create cart',
        # 'cart_read': 'Read cart',
        # 'cart_update': 'Update cart',
        # 'cart_delete': 'Delete cart',

        # #favorites
        # 'favorites_create': 'Create favorites',
        # 'favorites_read': 'Read favorites',
        # 'favorites_update': 'Update favorites',
        # 'favorites_delete': 'Delete favorites',

        #common
        'common_read': 'Read common resources',

        #warehouse
        'warehouse_create': 'Create warehouse items',
        'warehouse_read': 'Read warehouse items',
        'warehouse_update': 'Update warehouse items',
        'warehouse_delete': 'Delete warehouse items',
    }
}

VNPAY = {
    'vnp_TmnCode': config('VNP_TMNCODE'),
    'vnp_HashSecret': config('VNP_HASHSECRET'),
    'vnp_Url': config('VNP_URL'),
    'vnp_ReturnUrl': config('VNP_RETURNURL'),
}

AUTH_USER_MODEL = 'users.Employee'

LOGIN_URL = '/api/auth/login/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',  
    # ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     
    'ROTATE_REFRESH_TOKENS': True,                  
    'BLACKLIST_AFTER_ROTATION': True,              
    'AUTH_HEADER_TYPES': ('Bearer',),               
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# AUTHENTICATION_BACKENDS = [
#     'oauth2_provider.backends.OAuth2Backend'
# ]

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
        'NAME': os.getenv('POSTGRES_DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
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

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
