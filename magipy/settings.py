"""
Django settings for magipy project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MAGI_SECRET_KEY', '^i377a$-k4zce3e%yah$!p&n)yaj_qlxkkz+x43v0!(pkux-qa')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('MAGI_PYTHON_ENV', 'development').lower() == 'development'

if not DEBUG: raise ValueError('MAGIPY in production mode is not fully implemented.')
ALLOWED_HOSTS = []
if 'MAGI_SITE_URL' in os.environ:
    ALLOWED_HOSTS.append( os.environ.get('MAGI_SITE_URL') )

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'annotations',
    'accounts'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'magipy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, "templates"))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
               'django.contrib.auth.context_processors.auth',
               'django.core.context_processors.debug',
               'django.core.context_processors.i18n',
               'django.core.context_processors.media',
               'django.core.context_processors.static',
               'django.core.context_processors.tz',
               'django.contrib.messages.context_processors.messages',
               'social.apps.django_app.context_processors.backends',
               'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
   'social.backends.google.GoogleOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('MAGI_GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('MAGI_GOOGLE_CLIENT_SECRET')
LOGIN_URL = '/account/login'
WSGI_APPLICATION = 'magipy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
        'NAME'    : os.environ.get('MAGI_POSTGRES_DB', 'magipy'),
        'USER'    : os.environ.get('MAGI_POSTGRES_USER', 'mdml'),
        'PASSWORD': os.environ.get('MAGI_POSTGRES_PASSWORD', ''),
        'HOST'    : os.environ.get('MAGI_POSTGRES_HOST', ''),
        'PORT'    : os.environ.get('MAGI_POSTGRES_PORT', '5432'),
        'client_encoding': 'UTF8',
        'default_transaction_isolation': 'read committed',
        'timezone': 'UTC'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
