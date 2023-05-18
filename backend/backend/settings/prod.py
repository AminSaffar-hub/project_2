from backend.settings.base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    "192.168.1.56",
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
        'NAME': os.getenv('POSTGRES_USER'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5400,
    }
}