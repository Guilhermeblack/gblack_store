"""
Django settings for gbstr project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import cloudinary  # cloudinary
import cloudinary.uploader  # cloudinary
import cloudinary.api  # cloudinary
import psycopg2.extensions
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
import django
from django.conf.global_settings import DATABASES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jz91+(t=#6sdlnsykv)b*f#op@-qv1j22=x-xg)hc$q7_8kurc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ajax',
    'pwa',
    'gbstr',
    'loja',
    'cloudinary',
    'django_pagarme',
    'paypal.standard.pdt',
    # 'django-heroku'
]
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE_CLASSES = (

    'whitenoise.middleware.WhiteNoiseMiddleware'
)

# django.setup()

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gbstr.urls'

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
                'django.template.context_processors.request'
            ],
        },
    },
]

WSGI_APPLICATION = 'gbstr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
client_encoding= 'UTF8'
timezone='America/Sao_Paulo'
default_transaction_isolation= 'read committed'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        # 'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

import dj_database_url
DATABASES['default'] = dj_database_url.config(default='postgres://bqutzjqhbzyeun:2a696be3f207322ebfba850995ca6ffd4f658b34664d2240a149803a9b9a4468@ec2-52-4-171-132.compute-1.amazonaws.com:5432/d185ti2fvcrrac')
# DATABASES['default'] = dj_database_url.config()

AUTH_USER_MODEL = "loja.Cliente"



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# django_heroku.settings(locals())

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')




STATIC_URL = '/static/'
MEDIA_URL = '/media/'


STATICFILES_DIRS = ( os.path.join(BASE_DIR, '/static/'), )
MEDIA_ROOT = os.path.join(BASE_DIR, 'loja/static/')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles')
# STATIC_ROOT = BASE_DIR / 'staticfiles'





# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'loja/static/'),
)

PWA_APP_NAME = 'GBlack'
PWA_APP_DESCRIPTION = "seu produto esta aqui"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/my_app_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/my_apple_icon.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'pt-BR'


cloudinary.config(
    cloud_name="gblack",
    api_key="191418815964556",
    api_secret="hvTxhjD4ZyfYigVrte6ucol0lio"
)

# Dados para integração com Pagarme
# CHAVE_PAGARME_API_PRIVADA = 'ak_live_8jUYbLG5ojzgs9wisry243ycehrk1g'
# CHAVE_PAGARME_CRIPTOGRAFIA_PUBLICA = 'ek_live_kwLtZhdUxIWxbGGC4cHq7cddKh5T21'
#
# # Para validar telefones no Brasil
# PHONENUMBER_DEFAULT_REGION = 'BR'

PAYPAL_IDENTITY_TOKEN= 'e2WYMTODkM8DQeoYvI4ODlA9e2ZaMzNHp5i2O64HTCc6TjZ1Bhz0g2UZdEe'
TKN_PAYPAL= 'e2WYMTODkM8DQeoYvI4ODlA9e2ZaMzNHp5i2O64HTCc6TjZ1Bhz0g2UZdEe'