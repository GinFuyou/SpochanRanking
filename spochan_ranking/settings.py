# -*- coding: utf-8 -*-
"""
Django settings for spochan_ranking project.

Generated by 'django-admin startproject' using Django 4.1.2.
Custom template ver.4.1.0-1-a3

# Using django-classy-settings 3.x
# https://django-classy-settings.readthedocs.io
"""
from os import environ
from pathlib import Path
from platform import python_version

from cbs import BaseSettings, env
from django import get_version as django_version
from django.utils.translation import gettext_lazy as _

from . import __version__

# from redis import StrictRedis  # for caches


ENV_PREFIX = 'SPOCHAN_RANKING_'

denv = env[ENV_PREFIX]

print(f"{environ.get('DJANGO_SETTINGS_MODULE')}")

PROJECT_VERSION = __version__
PROJECT_NAME = "Spochan_Ranking"
DJANGO_VERSION = django_version()


TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = [('en-UK', _('English')),
             ('ru-RU', _('Russian')), ]

AUTH_USER_MODEL = 'core.CoreUser'
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

WSGI_APPLICATION = 'spochan_ranking.wsgi.application'

ROOT_URLCONF = 'spochan_ranking.urls'

SITE_ID = 1

STYLES_APP = 'core'
CELESTIA_STATIC_APPS = ('core', )

MAIN_STYLE_FILENAME = 'main'


class Settings(BaseSettings):
    DEBUG = denv(True)

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = env('django-insecure-l+sg31=edm5a0i+_@k0%*fs@&fr16cx$z-cdnlk&v#v#w^od*q')

    BASE_DIR = Path(__file__).resolve().parent.parent

    INTERNAL_IPS = ['127.0.0.1', '192.168.2.49']
    ALLOWED_HOSTS = []

    def INSTALLED_APPS(self):
        apps = (
            'core.apps.CoreConfig',
            'certification.apps.CertConfig',
            'chanbara.apps.ChanbaraConfig',
            'celestia',
            # 'simple_history',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.sites',  # needed for sitemap framework
            'debug_toolbar' if self.DEBUG else None,
            'django_extensions' if self.DEBUG else None,
            'django.contrib.staticfiles',
            'qr_code',
        )
        return [i for i in apps if i]

    def MIDDLEWARE(self):
        middlewares = (
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'debug_toolbar.middleware.DebugToolbarMiddleware' if self.DEBUG else None,
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            # 'simple_history.middleware.HistoryRequestMiddleware',
        )
        return [i for i in middlewares if i]

    # def LOCALE_PATHS(self):
    #     return [self.BASE_DIR / 'locale', ]

    """
    CACHES = {
        "default": {"BACKEND": "django_redis.cache.RedisCache",
                    "LOCATION": "redis://127.0.0.1:{port}/{db}".format(port=6379, db=REDIS_DB_DICT['cache']),
                    "KEY_PREFIX": "_spochan_ranking_",
                    "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient",}}  }

    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    """
    """
    SETTING_CONTEXT_NAMES = (
        'PROJECT_VERSION',
        'SCRIPTS',
        'STYLES'
    )
    """

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
                    # 'celestia.context_processors.setting',
                ],
            },
        },
    ]  # END TEMPLATES

    SHELL_PLUS_IMPORTS = ["from django.apps import apps"]

    WEB_ROOT = denv(Path("/Setsuna/web/spochan_ranking/"))  # arg is default for env var

    def STATIC_ROOT(self):
        return self.WEB_ROOT / 'static/'

    def MEDIA_ROOT(self):
        return self.WEB_ROOT / 'media/'

    STATIC_URL = '/static/'

    FONTAWESOME_VERSION = "v5.8.2"
    FONTAWESOME_CDN = (
        f"https://use.fontawesome.com/releases/{FONTAWESOME_VERSION}/css/all.css",
        "sha384-oS3vJWv+0UjzBfQzYUhtDYW+Pj2yciDJxpsK1OYPAYjqT085Qq/1cq5FLXAZQ7Ay", )
    FONTAWESOME_JS_CDN = (
        f"https://use.fontawesome.com/releases/{FONTAWESOME_VERSION}/js/all.js",
        "sha384-DJ25uNYET2XCl5ZF++U8eNxPWqcKohUUBUpKGlNLMchM7q4Wjg2CUpjHLaL8yYPH", )
    JQUERY_CDN = "//code.jquery.com/jquery-2.2.4.min.js"
    JQUERY_HASH = "sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="

    def DATABASES(self):
        return {'default':
                    {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': self.BASE_DIR / 'spochan_ranking.sqlite3',
                    }
                }


class DevSettings(Settings):
    pass


class ProdSettings(Settings):
    # DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ALLOWED_HOSTS = ['test.example.com', ]  # WARNING fill in hosts

    DEBUG = denv(False)

    DATABASES = {
        'default':
            {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'spochan_ranking',
            },
    }  # END DATABASES

    WEB_ROOT = denv(Path("/srv/web/spochan_ranking/"))


# Apply CBS 3+

# The `use` method will find the right sub-class of ``BaseSettings`` to use
# Based on the value of the `DJANGO_MODE` env var.
__getattr__, __dir__ = BaseSettings.use()

DJANGO_MODE = environ.get('DJANGO_MODE', 'Dev')

print(f"{PROJECT_NAME.replace('_', '')} v.{PROJECT_VERSION}"
      f" on python {python_version()} [{DJANGO_MODE}] DEBUG=N/A")  # TODO add .select() when implemented
