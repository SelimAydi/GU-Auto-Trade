"""
Django settings for guautotrade project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from os.path import join

import oscar
from django.urls import reverse_lazy, reverse
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar import get_core_apps
from oscar.defaults import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k^_-a^0mocfym(l*y-(!a=i2@hgmuz=bxf4qoxyd0ko+q4yrwe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/shelby/shop/accounts/profile'
LOGIN_URL ='/shelby/shop/accounts/login'

SITE_ID = 2

THUMBNAIL_FORMAT = 'PNG'

OSCAR_DEFAULT_CURRENCY = 'EUR'

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

# Application definition

INSTALLED_APPS = [
    'django_countries',
    'paypal',
    'modeltranslation',
	'appgu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.sites',
	'django.contrib.flatpages',
    'compressor',
    'widget_tweaks',
] + get_core_apps(['appgu.oscar.checkout', 'appgu.oscar.order', 'appgu.oscar.partner', 'appgu.oscar.shipping'])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'guautotrade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'appgu/templates'),
            location('../appgu/templates'),
			location('../appgu/templates/oscar'),
        ],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

				'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'guautotrade.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'guautodb2',
		'USER': 'postgres',
		'PASSWORD': 'kaas123',
		'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

# AUTH_USER_MODEL = 'appgu.dealers'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
		'OPTIONS': {
            'min_length': 5,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_SHOP_NAME = 'Shelby Webshop'
OSCAR_PROMOTIONS_ENABLED = False

OSCAR_HOMEPAGE = reverse_lazy('catalogue:index')
OSCAR_FROM_EMAIL = 'info@guautotrade.com'
OSCAR_SHOP_TAGLINE = 'Shelby Merchandise'
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Dutch'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = '/static/'
STATIC_URL = STATIC_ROOT

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SEND_GRID_API_KEY = ''
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'guautotrade'
EMAIL_HOST_PASSWORD = 'Auto2018!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@guautotrade.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Paypal settings
# PAYPAL_API_USERNAME = 'uitbetaling-facilitator_api1.wemoney.nl'
# PAYPAL_API_PASSWORD = 'PXZSY2PNZ3GWPYJQ'
# PAYPAL_API_SIGNATURE = 'A5rbR..nAsPB.9eX2Kko49PtM-AMAceoxw6B-EToi4q6Z5VRDP4lWLVp'
# SECURE_SSL_REDIRECT = False

ORDER_STATUS_PAID = 'Being processed'

# Oscar Shop settings
OSCAR_INITIAL_ORDER_STATUS = OSCAR_INITIAL_LINE_STATUS = 'Pending Payment'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Open': ('Pending Payment', 'Cancelled', 'Paid', 'Failed'),
    'Pending Payment': ('Cancelled', 'Paid', 'Failed'),
    'Cancelled': (),
    'Paid': (),
    'Failed': (),
}

ORDER_PENDING_STATUS = 'Pending'
ORDER_CANCELLED_STATUS = 'Cancelled'
ORDER_FAILED_STATUS = 'Failed'
ORDER_OPEN_STATUS = 'Open'
ORDER_PAID_STATUS = 'Paid'

# Mollie settings
OSCAR_MOLLIE_CONFIRMED_STATUSES = [ORDER_STATUS_PAID, 'Paid'],
OSCAR_MOLLIE_HTTPS = False
MOLLIE_API_KEY = 'test_cCKc9q6jPNxb8MM7ta2uuNs2s5Wp79'
MOLLIE_STATUS_MAPPING = {
    'Open': 'Open',
    'Paid': 'Paid',
    'Pending': 'Pending Payment',
    'Cancelled': 'Cancelled',
    'Failed': 'Failed'
}

# Production settings
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = "DENY"