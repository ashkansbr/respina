from .base import *

DEBUG = True


ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'respina',
        'USER': 'respina',
        'PASSWORD': '12345678',
        'HOST': 'db',
        'PORT': '5432',
    }
}
