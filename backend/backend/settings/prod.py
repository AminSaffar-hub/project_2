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


CSRF_TRUSTED_ORIGINS = ["https://erradar.com"]


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_NAME")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS")
