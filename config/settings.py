"""
╔══════════════════════════════════════════════════════════╗
║  AUTOINFO - DJANGO SETTINGS (WITH i18n + ROSETTA)       ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/config/settings.py                 ║
║  Multi-language support enabled                          ║
╚══════════════════════════════════════════════════════════╝
"""

from pathlib import Path
import os

# ═══════════════════════════════════════════════════════
# BASE DIRECTORY
# ═══════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════
# SECURITY
# ═══════════════════════════════════════════════════════
SECRET_KEY = 'django-insecure-change-this-in-production-k8w2m#n@x!7p$v9&q3a'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# ═══════════════════════════════════════════════════════
# INSTALLED APPS
# ═══════════════════════════════════════════════════════
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'rosetta',  # Translation management
    'rest_framework',
    'corsheaders',
    'django_filters',

    # Mūsų Apps
    'apps.core.apps.CoreConfig',
]

# ═══════════════════════════════════════════════════════
# MIDDLEWARE
# ═══════════════════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ← Language support!
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ═══════════════════════════════════════════════════════
# TEMPLATES
# ═══════════════════════════════════════════════════════
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'apps' / 'core' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # ← i18n support!
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ═══════════════════════════════════════════════════════
# DATABASE - POSTGRESQL
# ═══════════════════════════════════════════════════════
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'autoinfo',
        'USER': 'autoinfo',
        'PASSWORD': 'autoinfo',  # PAKEISK ČIA!
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ═══════════════════════════════════════════════════════
# PASSWORD VALIDATION
# ═══════════════════════════════════════════════════════
AUTH_PASSWORD_VALIDATORS = []

# ═══════════════════════════════════════════════════════
# INTERNATIONALIZATION (MULTI-LANGUAGE)
# ═══════════════════════════════════════════════════════
LANGUAGE_CODE = 'en'  # Default language (admin will use this)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('en', 'English'),
    ('lt', 'Lietuvių'),
    ('lv', 'Latviešu'),
    ('pl', 'Polski'),
    ('de', 'Deutsch'),
    ('ru', 'Русский'),
    ('es', 'Español'),
    ('fr', 'Français'),
]

# Locale paths for translations
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ═══════════════════════════════════════════════════════
# ROSETTA TRANSLATION SETTINGS
# ═══════════════════════════════════════════════════════
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_MESSAGES_PER_PAGE = 20
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
ROSETTA_REQUIRE_AUTH = True
ROSETTA_AUTO_COMPILE = True
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = 'en'
ROSETTA_WSGI_AUTO_RELOAD = True
ROSETTA_UWSGI_AUTO_RELOAD = False

# ═══════════════════════════════════════════════════════
# STATIC FILES
# ═══════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'apps' / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ═══════════════════════════════════════════════════════
# MEDIA FILES
# ═══════════════════════════════════════════════════════
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ═══════════════════════════════════════════════════════
# DEFAULT PRIMARY KEY
# ═══════════════════════════════════════════════════════
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ═══════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ═══════════════════════════════════════════════════════
# SESSION CONFIGURATION (Remember Me support)
# ═══════════════════════════════════════════════════════
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds (default Django value)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Don't expire by default (controlled by view)
SESSION_SAVE_EVERY_REQUEST = False  # Only update session when modified
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# ═══════════════════════════════════════════════════════
# API KEYS
# ═══════════════════════════════════════════════════════
CHEAPCARFAX_API_KEY = 'tl9kx8yxkuc'
CHEAPCARFAX_API_URL = 'https://panel.cheapcarfax.net/api'

CARFAX_API_KEY = ''
CARFAX_API_URL = 'https://api.carfax.com'
AUTOCHECK_API_KEY = ''
AUTOCHECK_API_URL = 'https://api.autocheck.com'
NMVTIS_API_KEY = ''
NMVTIS_API_URL = 'https://api.nmvtis.com'

# ═══════════════════════════════════════════════════════
# REPORT PRICES (EUR)
# ═══════════════════════════════════════════════════════
REPORT_PRICES = {
    'autocheck': {'single': 12.99, 'pack_10': 11.99, 'pack_100': 8.99},
    'carfax': {'single': 14.99, 'pack_10': 12.99, 'pack_100': 9.99},
    'nmvtis': {'single': 19.99, 'pack_10': 16.99, 'pack_100': 13.99}
}

# ═══════════════════════════════════════════════════════
# STRIPE
# ═══════════════════════════════════════════════════════
STRIPE_PUBLIC_KEY = ''
STRIPE_SECRET_KEY = ''
STRIPE_WEBHOOK_SECRET = ''

# ═══════════════════════════════════════════════════════
# EMAIL CONFIGURATION (Gmail SMTP)
# ═══════════════════════════════════════════════════════
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'romasm3@gmail.com'  # ← JŪSŲ GMAIL
EMAIL_HOST_PASSWORD = 'otcjtoemearnomdz'  # ← ČIA REIKIA APP PASSWORD!
DEFAULT_FROM_EMAIL = 'AutoInfo <romasm3@gmail.com>'

# ═══════════════════════════════════════════════════════
# REST FRAMEWORK
# ═══════════════════════════════════════════════════════
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ═══════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {'handlers': ['file'], 'level': 'INFO'},
    },
}
