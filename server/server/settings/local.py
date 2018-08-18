from .base import *
DEBUG = True

SECRET_KEY='local'
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'goodbullapi',
        'USER': 'goodbulldev',
        'PASSWORD': 'developer',
        'HOST': 'localhost',
        'PORT': ''
    }
}