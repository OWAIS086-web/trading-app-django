

from pathlib import Path
import os
import io
from os.path import abspath, basename, dirname
import environ
import logging
import json
import base64
import binascii
import google.auth
from google.oauth2 import service_account
from google.cloud import secretmanager
from google.auth.exceptions import DefaultCredentialsError
from google.api_core.exceptions import PermissionDenied
from modules.manifest import get_modules
from django.utils.translation import gettext_lazy as _
import atexit  # Add this import
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import subprocess
# from datetime import timedelta
import pytz


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()
env.read_env(env_file)

########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name.
SITE_NAME = basename(DJANGO_ROOT)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "secret_key")
ADMIN_CHARTS_USE_JSONFIELD = False
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

if not DEBUG:
    try:
        # Pull secrets from Secret Manager
        _, project = google.auth.default()
        client = secretmanager.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
        name = client.secret_version_path(project, settings_name, "latest")
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        env.read_env(io.StringIO(payload))
    except (DefaultCredentialsError, PermissionDenied):
        pass


ALLOWED_HOSTS = []
SITE_ID = 1

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("SECURE_REDIRECT", default=False)

# Application definition

INSTALLED_APPS = [
    'admin_volt.apps.AdminVoltConfig',
    # 'admin_tools_stats',  
    'django_nvd3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    'settings',
   

]
LOCAL_APPS = [
    "home.apps.HomeConfig",
    "portfolio.apps.PortfolioConfig",
    "users.apps.UsersConfig",
    'api_modules.apps.ApiModulesConfig',
    "subscriptions.apps.SubscriptionsConfig",
]

THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "django_extensions",
    "fcm_django",
    "import_export",
    "django_filters",
    "cities_light",
    "crispy_forms",
    "crispy_bootstrap5",
    "bootstrap5",

    "django_rest_passwordreset",

    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework",
    "rest_framework.authtoken",
    'rest_auth',
    
]

# MODULES_APPS = []
MODULES_APPS = get_modules()

INSTALLED_APPS += LOCAL_APPS
INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += MODULES_APPS

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'master.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "web_build"),
            os.path.join(BASE_DIR,"admin_volt/templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.contrib.sites.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'master.wsgi.application'

# one signal keys
ONE_SIGNAL_APP_ID = env.str("ONE_SIGNAL_APP_ID", "")
ONE_SIGNAL_API_KEY = env.str("ONE_SIGNAL_API_KEY", "")


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_ENGINE = env.str("DATABASE_ENGINE", default=None)
DATABASE_NAME = env.str("DATABASE_NAME", default=None)
DATABASE_USER = env.str("DATABASE_USER", default=None)
DATABASE_PASSWORD = env.str("DATABASE_PASSWORD", default=None)
DATABASE_HOST = env.str("DATABASE_HOST", default=None)
DATABASE_PORT = env.str("DATABASE_PORT", default=None)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "pgpdb.sqlite3",
        # 'ENGINE':env.str("DATABASE_ENGINE", default=None),
        # 'NAME':env.str("DATABASE_NAME", default=None),
        # 'USER':env.str("DATABASE_USER", default=None),
        # 'PASSWORD':env.str("DATABASE_PASSWORD", default=None),
        # 'HOST':env.str("DATABASE_HOST", default=None),
        # 'PORT':env.str("DATABASE_PORT", default=None),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "web_build/static"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# allauth / users
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_UNIQUE_EMAIL = True


# LOGIN_REDIRECT_URL = "users:redirect"
# LOGIN_REDIRECT_URL = "/"
#UPDATE KRNA HY FROM USERS:URLS....
# LOGOUT_REDIRECT_URL = "users:redirect"
LOGOUT_REDIRECT_URL = "/"
POST_CHANGE_REDIRECT_URL = 'password_change_done'




ACCOUNT_ADAPTER = "users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "users.adapters.SocialAccountAdapter"
ACCOUNT_ALLOW_REGISTRATION = env.bool("ACCOUNT_ALLOW_REGISTRATION", True)
SOCIALACCOUNT_ALLOW_REGISTRATION = env.bool("SOCIALACCOUNT_ALLOW_REGISTRATION", True)

REST_AUTH_SERIALIZERS = {
    # Replace password reset serializer to fix 500 error
    "PASSWORD_RESET_SERIALIZER": "users.accounts.api.v1.serializers.PasswordSerializer",
}
REST_AUTH_REGISTER_SERIALIZERS = {
    # Use custom serializer that has no username and matches web signup
    "REGISTER_SERIALIZER": "users.accounts.api.v1.serializers.SignupSerializer",
}


# Custom user model
AUTH_USER_MODEL = "users.User" # changes the built-in user model to ours


# SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mathew.10399376@gmail.com'
EMAIL_HOST_PASSWORD = 'nazljlaivmmuitig'


# Swagger settings for api docs
SWAGGER_SETTINGS = {
    "DEFAULT_INFO": f"{ROOT_URLCONF}.api_info",
}

if DEBUG or not (EMAIL_HOST_USER and EMAIL_HOST_PASSWORD):
    # output email to console instead of sending
    if not DEBUG:
        logging.warning("You should setup `SENDGRID_USERNAME` and `SENDGRID_PASSWORD` env vars to send emails.")
    # EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# GCP config
def google_service_account_config():
    # base64 encoded service_account.json file
    service_account_config = env.str("GS_CREDENTIALS", "")
    if not service_account_config:
        return {}
    try:
        return json.loads(base64.b64decode(service_account_config))
    except (binascii.Error, ValueError):
        return {}


GOOGLE_SERVICE_ACCOUNT_CONFIG = google_service_account_config()
if GOOGLE_SERVICE_ACCOUNT_CONFIG:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(GOOGLE_SERVICE_ACCOUNT_CONFIG)
GS_BUCKET_NAME = env.str("GS_BUCKET_NAME", "")
if GS_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    # STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"

# rest framework settings
# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated', ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 20,
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'api_modules.authentication.CustomTokenAuthentication',
#         'rest_framework.authentication.SessionAuthentication',  # Use session authentication for simplicity
#         'rest_framework.authentication.TokenAuthentication',    # Token authentication for API access
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ],
#     'DEFAULT_FILTER_BACKENDS': [
#         'django_filters.rest_framework.DjangoFilterBackend',
#         'rest_framework.filters.SearchFilter',
#         'rest_framework.filters.OrderingFilter',
#     ]
# }



# corsheaders settings
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=True)

# Debug toolbar settings
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
    }

# one signal keys
ONE_SIGNAL_APP_ID = env.str('ONE_SIGNAL_APP_ID', '')
ONE_SIGNAL_API_KEY = env.str('ONE_SIGNAL_API_KEY', '')

# FCM_DJANGO_SETTINGS
FCM_SERVER_KEY = env.str('FCM_SERVER_KEY', "")
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": FCM_SERVER_KEY,
    # 'DELETE_INACTIVE_DEVICES': False,
    # 'ONE_DEVICE_PER_USER': False,
    # 'UPDATE_ON_DUPLICATE_REG_ID': True,
}

# stripe env settings
STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY', 'pk_test_YOUR_KEY')
STRIPE_LIVE_SECRET_KEY = os.environ.get('STRIPE_LIVE_SECRET_KEY', default=None)

STRIPE_TEST_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLIC_KEY', 'pk_test_YOUR_KEY')
STRIPE_LIVE_PUBLIC_KEY = os.environ.get('STRIPE_LIVE_PUBLIC_KEY', default=None)

STRIPE_TEST_PUBLISHABLE_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY', 'pk_test_YOUR_KEY')
STRIPE_LIVE_PUBLISHABLE_KEY = os.environ.get('STRIPE_LIVE_PUBLISHABLE_KEY', default=None)
# Change to True in production
STRIPE_LIVE_MODE = env.bool('STRIPE_LIVE_MODE', default=False)
# Get it from the section in the Stripe dashboard where ou added the webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = env.str('DJSTRIPE_WEBHOOK_SECRET', '')
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# apple store connect env variables
APP_STORE_BUNDLE_ID = env.str('APP_STORE_BUNDLE_ID', 'com.crowdbotics.analog')
APP_STORE_KEY_ID = env.str('APP_STORE_KEY_ID', '1645494808')
APP_STORE_APPLE_ID = env.str('APP_STORE_APPLE_ID', '1645494808')
APP_STORE_API_LIVE_MODE = env.bool('APP_STORE_API_LIVE_MODE', default=False)
APP_STORE_PRIVATE_KEY = env.str('APP_STORE_PRIVATE_KEY', '')
APP_STORE_SKU = env.str('APP_STORE_SKU', '')
APP_STORE_ISSUER_ID = env.str('APP_STORE_ISSUER_ID', '')
APP_STORE_IN_APP_SHARED_SECRET = env.str('APP_STORE_IN_APP_SHARED_SECRET', '')

REST_USE_JWT = True  # If you want to use JWT authentication

AUTHENTICATION_CLASSES = [
    'dj_rest_auth.authentication.AllAuthJWTAuthentication',
    # Add any other authentication classes you need
]
AUTHENTICATION_CLASSES += ['dj_rest_auth.authentication.AllAuthJWTAuthentication']
