# zipcab_project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# --------------------------------------
# BASE DIR
# --------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------
# LOAD ENV
# --------------------------------------
load_dotenv(BASE_DIR / ".env")

DJANGO_ENV = os.getenv("DJANGO_ENV", "local")

# --------------------------------------
# SECRET & DEBUG
# --------------------------------------
API_KEY = os.getenv("API_KEY","error")
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]  # Allow all hosts for development

# --------------------------------------
# INSTALLED APPS
# --------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "silk" ,
    "api.apps.ApiConfig",
]



# --------------------------------------
# MIDDLEWARE
# --------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # place CORS middleware always at the first place 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware"
]

# Silk middleware only for local / admin
if DJANGO_ENV == "local":
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")

# --------------------------------------
# URL CONFIG
# --------------------------------------
ROOT_URLCONF = "zipcab_project.urls"

# --------------------------------------
# TEMPLATES
# --------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend" / "dist"],  # React build
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "zipcab_project.wsgi.application"

# --------------------------------------
# DATABASE
# --------------------------------------
if DJANGO_ENV == "production":
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL)
}
#permission classes

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# --------------------------------------
# PASSWORD VALIDATORS
# --------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# --------------------------------------
# INTERNATIONALIZATION
# --------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------
# STATIC & MEDIA
# --------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / '../frontend/dist',
]


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-render-service-name.onrender.com']

CORS_ALLOW_ALL_ORIGINS = True # development only change it when deploying
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-name.onrender.com',
    'http://localhost:5173',
]
CORS_ALLOW_CREDENTIALS = True 
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
    "user-agent",
    "dnt",
    "x-csrftoken",
    "x-requested-with",
]