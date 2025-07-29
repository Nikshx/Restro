# In backend/settings.py

from datetime import timedelta
from pathlib import Path
import os

# --- 1. THE CORRECT BASE_DIR ---
# This is the path to your project root (the folder containing manage.py)
# Based on your feedback, it needs to go up three levels from settings.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-=jn$5p5t5i(7_rd!1o_9pp7mtyvt-pfbm1skiadh16k_$qvq8^"
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "base",
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend', 'dist')],
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

WSGI_APPLICATION = "backend.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- 2. THE CORRECT STATIC FILES CONFIGURATION ---
STATIC_URL = '/static/'

# This is the directory where `collectstatic` will place all files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# This tells `collectstatic` where to find your React build assets.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/dist'),
]
# --- END OF STATIC FIX ---

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # For your React dev server
    "http://127.0.0.1:5173",   # For your React dev server
    "http://localhost:8000",  # For when you visit localhost:8000
    "http://127.0.0.1:8000",   # <-- THIS IS THE MISSING LINE
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",   # <-- ADD THIS LINE HERE AS WELL
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',)
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

UNSPLASH_ACCESS_KEY = "bRSY6Ar9PUb1986rvzrDGYSX2ZUpbq7JF1x_mapdeTk"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-canteen-cache',
    }
}