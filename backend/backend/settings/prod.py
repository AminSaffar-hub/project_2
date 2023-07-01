from backend.settings.base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    "erradar.com",
    "localhost",
    "host.docker.internal",
    "13.38.188.241",
]

STATIC_ROOT = "/www/static/"
STATIC_URL = "/static/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_USER"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5400,
    }
}
