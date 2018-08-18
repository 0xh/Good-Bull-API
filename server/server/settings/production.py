from .base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*.goodbullschedules.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASS'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': ''
    }
}

ADMINS = [('Gabriel', 'quontas@gmail.com')]
