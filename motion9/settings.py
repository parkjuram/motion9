"""
Django settings for motion9 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/'
)

CHARSET = 'utf-8'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'atgl$8^42a$nspf0@9o9t6-*$33foid5nlxl0fzt!@*_%cl1e5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'web',
    'mobile',
    'users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'motion9.urls'

WSGI_APPLICATION = 'motion9.wsgi.application'


# Logging

from datetime import datetime

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file_all': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': datetime.now().strftime('log/all_%d_%m_%Y.log'),
            'formatter': 'verbose'
        },
        'file_common_controller': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': datetime.now().strftime('log/common_controller_%d_%m_%Y.log'),
            'formatter': 'verbose'
        },
        'file_web': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': datetime.now().strftime('log/web_%d_%m_%Y.log'),
            'formatter': 'verbose'
        },
        'file_mobile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': datetime.now().strftime('log/mobile_%d_%m_%Y.log'),
            'formatter': 'verbose'
        },
        'file_users': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': datetime.now().strftime('log/users_%d_%m_%Y.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'common_controller': {
            'handlers': ['file_all', 'file_common_controller'],
            'level': 'DEBUG',
        },
        'web': {
            'handlers': ['file_all', 'file_web'],
            'level': 'DEBUG',
        },
        'mobile': {
            'handlers': ['file_all', 'file_mobile'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['file_all', 'file_users'],
            'level': 'DEBUG',
        },
    }
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'motion9',
        'USER': 'arsdale',
        'PASSWORD': 'gksehrjs0710',
        'HOST': '175.126.82.107',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, '../media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

# Login
LOGIN_URL = '/users/login_page/'