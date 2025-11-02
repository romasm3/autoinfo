"""
╔══════════════════════════════════════════════════════════╗
║  AUTOINFO - DJANGO SETTINGS (SIMPLIFIED)                ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/config/settings.py                 ║
║  BE python-decouple - tiesioginės reikšmės              ║
╚══════════════════════════════════════════════════════════╝
"""

from pathlib import Path
import os

# ═══════════════════════════════════════════════════════
# BASE DIRECTORY
# ═══════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════
# SECURITY - PAKEISK ŠIĄ REIKŠMĘ PRODUCTION!!!
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
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ═══════════════════════════════════════════════════════
# TEMPLATES - PATAISYTA! Ieško abiejose vietose
# ═══════════════════════════════════════════════════════
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Root level templates
            BASE_DIR / 'apps' / 'core' / 'templates',  # App templates
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ═══════════════════════════════════════════════════════
# DATABASE - SQLITE (development) arba POSTGRESQL
# ═══════════════════════════════════════════════════════

# VARIANTAS 1: SQLite (lengviausia pradžiai)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# VARIANTAS 2: PostgreSQL (atkomentuok kai reikės)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'autoinfo',
#         'USER': 'autoinfo_user',
#         'PASSWORD': 'your_password',  # PAKEISK
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# ═══════════════════════════════════════════════════════
# PASSWORD VALIDATION
# ═══════════════════════════════════════════════════════
AUTH_PASSWORD_VALIDATORS = []

# ═══════════════════════════════════════════════════════
# INTERNATIONALIZATION
# ═══════════════════════════════════════════════════════
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

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
# API KEYS (DEMO MODE)
# ═══════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════
# API KEYS - CheapCarfax Integration
# ═══════════════════════════════════════════════════════
CHEAPCARFAX_API_KEY = '8mpzhh9qfnp'  # Įrašyk savo API key čia
CHEAPCARFAX_API_URL = 'https://panel.cheapcarfax.net/api'

# Kiti API (ateičiai)
CARFAX_API_KEY = ''
CARFAX_API_URL = 'https://api.carfax.com'
AUTOCHECK_API_KEY = ''
AUTOCHECK_API_URL = 'https://api.autocheck.com'
NMVTIS_API_KEY = ''
NMVTIS_API_URL = 'https://api.nmvtis.com'

# ═══════════════════════════════════════════════════════
# REPORT PRICES (PLN)
# ═══════════════════════════════════════════════════════
REPORT_PRICES = {
    'autocheck': {'single': 12.99, 'pack_10': 11.99, 'pack_100': 8.99},
    'carfax': {'single': 14.99, 'pack_10': 12.99, 'pack_100': 9.99},
    'nmvtis': {'single': 19.99, 'pack_10': 16.99, 'pack_100': 13.99}
}

# ═══════════════════════════════════════════════════════
# STRIPE (jei reikės)
# ═══════════════════════════════════════════════════════
STRIPE_PUBLIC_KEY = ''
STRIPE_SECRET_KEY = ''

# ═══════════════════════════════════════════════════════
# EMAIL (Console backend - development)
# ═══════════════════════════════════════════════════════
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
