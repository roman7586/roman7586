"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4i$f_y6964w+t(k_u)5zng@y46kiw7vvlk$8*2%7!&!&$e6#v)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    'news',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    'django_apscheduler',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
    
]

ROOT_URLCONF = 'NewsPaper.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #ссылка на базу
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

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/accounts/login/' # Авторизация через allauth
LOGIN_REDIRECT_URL = '/news/indexx/' # перенаправление на страницу для авторизованного пользователя
ACCOUNT_LOGOUT_REDIRECT_URL ="/accounts/login" #перенаправление на страницу авторизации после выхода их профиля

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True # было до 6.2 ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  #было до 6.2 ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_FORMS = {'signup': 'news.forms.BasicSignupForm'}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'hiromant86'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = '2xcanonx2'  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru' #можно указать полностью адрес 'hiromant86@yandex.ru' . Для 6.2
#ACCOUNT_CONFIRM_EMAIL_ON_GET = True - позволит избежать дополнительных действий и активирует аккаунт сразу, как только мы перейдем по ссылке
#ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS  - количество дней, в течение которых будет доступна ссылка на подтверждение регистрации


CELERY_BROKER_URL = 'redis://default:T6awm2b9kCjXPDKe3mM4Qr9zKuU25Txq@redis-17198.c9.us-east-1-4.ec2.cloud.redislabs.com:17198'
CELERY_RESULT_BACKEND = 'redis://redis-17198.c9.us-east-1-4.ec2.cloud.redislabs.com:17198'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

LOGGING = {
     'version': 1,
     'disable_existing_loggers': False,
     'style' : '{',
     'formatters': {
         'simple': {
             'format': '%(asctime)s %(levelname)s %(message)s'
         },
         'verbose': {
             'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(process)d %(thread)d %(message)s'
         },
         'errorformat': {
             'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(process)d %(thread)d %(message)s %(exc_info)s'
         },
         'infoformat': {
             'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
         },
         'error_file_format': {
             'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s %(exc_info)s'
         },
         'securityformat': {
             'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
         },
         'mailformat': {
             'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s'
         },
     },
     'filters': {
         'require_debug_true': {
             '()': 'django.utils.log.RequireDebugTrue',
         },
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse',
         },
     },
     'handlers': {
         'console': {
            'level': 'DEBUG',
             'filters': ['require_debug_true'],
             'class': 'logging.StreamHandler',
             'formatter': 'simple'
         },
         'console_warning': {
             'level': 'WARNING',
             'filters': ['require_debug_true'],
             'class': 'logging.StreamHandler',
             'formatter': 'verbose'
         },
         'console_error': {
             'level': 'ERROR',
             'filters': ['require_debug_true'],
             'class': 'logging.StreamHandler',
             'formatter': 'verbose'
         },
         'file_info': {
             'level': 'INFO',
             'filters': ['require_debug_false'],
             'class': 'logging.FileHandler',
             'filename': 'general.log',
             'formatter': 'infoformat',
         },
         'file_error': {
             'level': 'ERROR',
             'class': 'logging.FileHandler',
             'filename': 'error.log',
             'formatter': 'error_file_format',
         },
         'file_security': {
             'level': 'INFO',
             'class': 'logging.FileHandler',
             'filename': 'security.log',
             'formatter': 'securityformat',
         },
         'mail_admins': {
             'level': 'ERROR',
             'filters': ['require_debug_false'],
             'class': 'django.utils.log.AdminEmailHandler',
             'formatter': 'mailformat',
         }
     },
     'loggers': {
         'django': {
             'handlers': ['console', 'console_warning', 'console_error', 'file_info'],
             'level': 'DEBUG',
             'propagate': True,
         },
         'django.request': {
             'handlers': ['mail_admins', 'file_error'],
             'level': 'ERROR',
             'propagate': False,
         },
         'django.server': {
             'handlers': ['mail_admins', 'file_error'],
             'level': 'ERROR',
             'propagate': False,
         },
         'django.template': {
             'handlers': ['file_error'],
             'level': 'ERROR',
             'propagate': False,
         },
         'django.db_backends': {
             'handlers': ['file_error'],
             'level': 'ERROR',
             'propagate': False,
         },
         'django.security': {
             'handlers': ['file_security'],
             'level': 'INFO',
             'propagate': False,
         }
     }
 }