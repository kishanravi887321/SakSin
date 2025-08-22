"""
Django settings for config project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from datetime import timedelta
from decouple import config

# Load .env variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET", "unsafe-secret")

# Debug mode (should be False in production)
DEBUG = config("DEBUG", default=False, cast=bool)

# Hosts allowed to serve the backend
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "sakin.onrender.com",
    "saksin.online",
    "www.saksin.online",
    "saksin-ui-nextjs.onrender.com",
]

# CORS
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "apps.accounts",
    "apps.interviews",
    "apps.subscriptions",
    "apps.analytics",
    "apps.central",  # LangChain Central Services
    "drf_yasg",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ✅ Must be very high
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://saksin-ui-nextjs.onrender.com",
    "http://localhost:3000",
    "https://saksin.online",
    "https://www.saksin.online",
    
    "https://saksin.vercel.app",
]
print(">>> Loaded settings.py with CORS:", CORS_ALLOWED_ORIGINS)
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "https://saksin-ui-nextjs.onrender.com",
    "https://sakin.onrender.com",
    "http://localhost:3000"
]
print('>>>>>  CSRF config >>>', CSRF_TRUSTED_ORIGINS)
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",
    "accept",
    "origin",
    "user-agent",
    "x-requested-with",
]
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ✅ central templates folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": dj_database_url.parse(
        os.getenv("DB_URL"), conn_max_age=600, ssl_require=True
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# DRF & JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "apps.accounts.serializers.CustomTokenObtainPairSerializer",
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(config("ACCESS_TOKEN_LIFETIME", default=5))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(config("REFRESH_TOKEN_LIFETIME", default=1))
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Cloudinary
import cloudinary

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer <token>'",
        }
    },
}

# Payments (Razorpay)
RAZORPAY_API_KEY = os.getenv("RAZORPAY_API_ID")
RAZORPAY_API_SECRET = os.getenv("RAZORPAY_API_SECRET")
RAZOR_PAY_RS = int(os.getenv("PAYMENT_AMOUNT_RS", default=100))

# Email/OTP
BREVO_API_KEY_EMAIL = os.getenv("BREVO_API_KEY_EMAIL")
FORWARDING_EMAIL = os.getenv("FORWARDING_EMAIL")

# Redis cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SSL": True,
        },
    }
}
REDIS_URL = os.getenv("REDIS_URL")

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
