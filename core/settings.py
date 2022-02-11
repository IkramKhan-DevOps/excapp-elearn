
from pathlib import Path
from decouple import config
import os

""" VAR ----------------------------------------------------------------------------------------"""
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'asdasasdsadasdsad2231231'
ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'accounts.User'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DEBUG = True
SERVER = False

if SERVER:
    if DEBUG:
        GOOGLE_CALLBACK_ADDRESS = "https://epay.pythonanywhere.com/accounts/google/login/callback/"
    else:
        GOOGLE_CALLBACK_ADDRESS = "https://epay.app/accounts/google/login/callback/"

    SITE_ID = 2
else:
    GOOGLE_CALLBACK_ADDRESS = "http://127.0.0.1:8000/accounts/google/login/callback/"
    SITE_ID = 1

ALLOWED_HOSTS = ['*']

""" APPS ---------------------------------------------------------------------------------------"""
INSTALLED_APPS = [
    # 'src.admins.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # REQUIRED_APPLICATIONS
    'crispy_forms',
    'ckeditor',
    'django_filters',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # CUSTOM APPS
    'src.website',
    'src.accounts',

    'src.portals.admins',
    'src.portals.customer',

    # END

]

""" MIDDLE WARES ----------------------------------------------------------------------------"""
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

""" TEMPLATES -------------------------------------------------------------------------------"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

""" DATABASES ------------------------------------------------------------------------------------"""
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'myproject',
            'USER': 'myprojectuser',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

""" VALIDATORS -----------------------------------------------------------------------------------"""

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

""" INTERNATIONALIZATION -------------------------------------------------------------------------"""

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" STATIC AND MEDIA ----------------------------------------------------------------------------"""

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

""" OTHER APPS SYSTEM ----------------------------------------------------------------------------"""
CRISPY_TEMPLATE_PACK = 'bootstrap4'

""" LOGIN SYSTEM ---------------------------------------------------------------------------------"""
LOGIN_REDIRECT_URL = '/accounts/cross-auth/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

""" EMAIL SYSTEM ---------------------------------------------------------------------------------"""

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'GIF': ".gif"
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

""" ALL-AUTH SETUP --------------------------------------------------------------------------------"""

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

ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
