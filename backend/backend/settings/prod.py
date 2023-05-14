from backend.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    "192.168.1.13",
    "localhost",
    "host.docker.internal",
    "ec2-52-47-128-70.eu-west-3.compute.amazonaws.com",
    "13.38.188.241",
]

STATIC_ROOT = "/www/static/"
STATIC_URL = "/static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': 5400,
    }
}