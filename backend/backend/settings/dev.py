from backend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    # for access from outside docker (when running in docker
    "0.0.0.0",
]

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

# debug email server, run with => python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
