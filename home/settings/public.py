import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z0yto1hircl%grs&)2x7jf0ey(w=p4z02!_ws9mm@3nfs7t(lo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DOMAIN_NAME = 'portal.sharkservers.pl'

ALLOWED_HOSTS = [DOMAIN_NAME]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'servers',
    'mainpage',
    'digg_paginator',
    'accounts',
    'shop',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'user_centrum',
    'profiles'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/home/sharkser/web/portal.sharkservers.pl/portal/public/templates'],
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

WSGI_APPLICATION = 'home.wsgi.public.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sharkser_portal',
        'USER': 'sharkser_portal',
        'PASSWORD': 'geOkY^dU50nXjbfi',
        'HOST': '54.37.233.204',
        'OPTIONS': {
        "init_command": "SET foreign_key_checks = 0;",
        },
    },
    #'jb_db': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'sharkser_jb',
    #    'USER': 'sharkser_jb',
    #    'PASSWORD': 'geOkY^dU50nXjbfi',
    #    'HOST': '54.37.233.204'
    #}
}


#DATABASE_ROUTERS = ['jailbreak.router.JailBreakRouter', ]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# STATICFILES_DIRS

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/sharkser/web/portal.sharkservers.pl/portal/public/media'
STATICFILES_DIRS = [
    "/home/sharkser/web/portal.sharkservers.pl/portal/public/static",
]
# LiveServer.pl Server Status Api
LS_API_SMS_URL = 'https://rec.liveserver.pl/api?channel=sms&return_method=http'
LS_API_PRZELEW_URL = 'https://rec.liveserver.pl/api?channel=online&return_method=http'
LS_CLIENT_ID = '645'
LS_CLIENT_PIN = '05a4da219ecea8a913e0eb28a07ffae8'
STEAM_API_KEY = '3EA42FC1689351CC71EE68045C84A5C3'
ABSOLUTE_URL = DOMAIN_NAME

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = (
    'accounts.backends.SteamBackend',
)

LOGIN_URL = '/login'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

API_URL = "http://" + DOMAIN_NAME + '/api'
