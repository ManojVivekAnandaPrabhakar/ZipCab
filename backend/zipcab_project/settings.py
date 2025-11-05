import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------------------------------
# BASE SETTINGS
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-temp-key")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".onrender.com"]
API_KEY=os.getenv("API_KEY","none")

# -----------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",
    "rest_framework",  # ✅ Needed for JWT
    "rest_framework_simplejwt",  # ✅ JWT support
    "silk",

    # Your apps
    "api",
]

# -----------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Always first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # ❌ Removed CsrfViewMiddleware (since JWT doesn’t use it)
    # "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "zipcab_project.urls"

# -----------------------------------------------------
# TEMPLATES
# -----------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "frontend" / "dist"],
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

# -----------------------------------------------------
# DATABASE CONFIG
# -----------------------------------------------------
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.parse(
            os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }

# -----------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------
# STATIC & MEDIA FILES
# -----------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR.parent / "frontend" / "dist"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------------------------------
# CORS CONFIG
# -----------------------------------------------------
CORS_ALLOW_CREDENTIALS = False  # ✅ JWT doesn’t need cookies

if os.getenv("DJANGO_ENV") == "production":
    CORS_ALLOWED_ORIGINS = [
        "https://zipcab-wgbm.onrender.com",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:5173",
    ]


# ❌ CSRF not needed
CSRF_TRUSTED_ORIGINS = []

# -----------------------------------------------------
# REST FRAMEWORK CONFIG
# -----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # ✅ Only JWT
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # ✅ Require auth by default
    ],
}

# -----------------------------------------------------
# LOGGING
# -----------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

# -----------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# -----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------
# FRONTEND BUILD (Optional)
# -----------------------------------------------------
FRONTEND_BUILD_DIR = BASE_DIR / "frontend" / "dist"
if FRONTEND_BUILD_DIR.exists():
    TEMPLATES[0]["DIRS"].append(FRONTEND_BUILD_DIR)
    STATICFILES_DIRS.append(FRONTEND_BUILD_DIR / "assets")
