#zipcab_project/settings.py
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()


# BASE DIRECTORY

BASE_DIR = Path(__file__).resolve().parent.parent


#the switch config 

DJANGO_ENV = os.getenv("DJANGO_ENV", "local")
if DJANGO_ENV == "production":
    load_dotenv(BASE_DIR / ".env.production")
else:
    load_dotenv(BASE_DIR / ".env.local")




SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true" #always keep debug = false, true if only need in development 
API_KEY = os.environ.get("API_KEY")


# ALLOWED HOSTS
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")



INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]


# MIDDLEWARE

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  #corsheaders middleware should be placed at top 
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  #
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
    


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}



ROOT_URLCONF = 'zipcab_project.urls'
WSGI_APPLICATION = 'zipcab_project.wsgi.application'


# TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


#this setting acts as a switch cause we cant debug with development settings 
#so change the variable and you're good to go in development "and the variable is in .env "

if DJANGO_ENV == "local":
    DATABASES = {
        'default': dj_database_url.parse(os.getenv("LOCAL_DATABASE_URL"))
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }



AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]




LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC FILES

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    # Path to the React build files copied by build.sh
    BASE_DIR / 'backend' / 'static' / 'frontend_build',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # regarding deployment for react 




MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


#for future updation 
#changeing the forgot password using email verification 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "ZipCab <noreply@zipcab.com>")


#drf configs

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}


#crosheaders config "important"


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5174",
# ]
CORS_ALLOW_ALL_ORIGINS = True # development only change it when deploying

CORS_ALLOW_CREDENTIALS = True  


#security configs for production 

if DJANGO_ENV == "production":
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
