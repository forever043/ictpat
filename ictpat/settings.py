"""
Django settings for ictpat project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c4l225ab4k2@ld_wrw9@l@d-fi-z9$#_r&149za+zt#xin=fbi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'libs.chartit',
    'django_nav',

    'dashboard',
    'patmgr',
    'scrmgr',
    'rankmgr',
    'sysmgr',

    'retrv',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'ictpat.urls'

WSGI_APPLICATION = 'ictpat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/ictpat.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/resources/'

STATIC_ROOT = os.path.join(BASE_DIR, 'resources')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'dashboard/resources'),
    os.path.join(BASE_DIR, 'patmgr/resources'),
    os.path.join(BASE_DIR, 'scrmgr/resources'),
    os.path.join(BASE_DIR, 'mgrutil/resources'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Messages
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
	message_constants.DEBUG: 'debug',
	message_constants.INFO: 'information',
	message_constants.SUCCESS: 'success',
	message_constants.WARNING: 'attention',
	message_constants.ERROR: 'error',
}

# Authentication
from django.core.urlresolvers import reverse
LOGIN_REDIRECT_URL = reverse('dashboard.views.dashboard')
LOGIN_URL = reverse('dashboard-login')
LOGOUT_URL = reverse('dashboard-logout')

#for filebrowsers
#FILEBROWSER_DIRECTORY = os.path.join(BASE_DIR, 'uploads')
PATENT_FILE_DIRECTORY = os.path.join(BASE_DIR, 'patent_files')

