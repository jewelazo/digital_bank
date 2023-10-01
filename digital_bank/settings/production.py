from .base import *

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME", default="postgres"),
        "USER": env("DATABASE_USER", default="postgres"),
        "PASSWORD": env("DATABASE_PASSWORD", default="none"),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": "5432",
    }
}
