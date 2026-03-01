"""
Django settings for blood_bank project.
Updated with Django REST Framework support.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xwdj(e468nd_z@heafh@-z1qn6z179va#hru-6gdq!5)pke#4c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bibhu.pythonanywhere.com', '*']


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps for REST API
    'rest_framework',                   # Django REST Framework ⭐
    'rest_framework.authtoken',         # Token authentication ⭐
    'django_filters',                   # Filtering support ⭐
    'corsheaders',                      # CORS headers ⭐
    'drf_spectacular',                  # API documentation ⭐
    
    # Your app
    'testapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',      # Static files ⭐
    'corsheaders.middleware.CorsMiddleware',           # CORS ⭐ (must be before CommonMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blood_bank.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'blood_bank.wsgi.application'


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blood_bank_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ==============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [STATIC_DIR]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# MEDIA FILES (User uploads)
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# REST FRAMEWORK CONFIGURATION ⭐ NEW
# ==============================================================================

REST_FRAMEWORK = {
    # Authentication Classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Token auth
        'rest_framework.authentication.SessionAuthentication',  # Session auth
    ],
    
    # Permission Classes
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    
    # Filtering Backends
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Renderer Classes
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Remove in production
    ],
    
    # Parser Classes
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    
    # Throttling (Rate Limiting)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',      # Anonymous users
        'user': '1000/hour',     # Authenticated users
    },
    
    # Schema Generation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # DateTime Format
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
}


# ==============================================================================
# DRF SPECTACULAR (API DOCUMENTATION) ⭐ NEW
# ==============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'Blood Bank Management System API',
    'DESCRIPTION': 'RESTful API for Blood Bank Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
}


# ==============================================================================
# CORS (Cross-Origin Resource Sharing) ⭐ NEW
# ==============================================================================

# Development Settings
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins in development
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Production Settings (Uncomment and configure for production)
# CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOWED_ORIGINS = [
#     "https://yourdomain.com",
#     "https://www.yourdomain.com",
# ]


# ==============================================================================
# LOGGING ⭐ NEW
# ==============================================================================

import os

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'debug.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'testapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# ==============================================================================
# AUTHENTICATION & SESSION
# ==============================================================================

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_HTTPONLY = True


# ==============================================================================
# SECURITY SETTINGS (PRODUCTION) - Commented out for development
# ==============================================================================

# Uncomment these for production deployment
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
