from pathlib import Path
from decouple import config
import os

# ========================
# BASE PATHS
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent


# ========================
# SECURITY (Load from .env)
# ========================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "dapurku.store",
    "www.dapurku.store",
    "127.0.0.1",
    "localhost",
]


# ========================
# INSTALLED APPS
# ========================
INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local Apps
    "users_db",
    "umkm",
]


# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ========================
# TEMPLATES
# ========================
ROOT_URLCONF = "karyacipta.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "karyacipta.wsgi.application"


# ========================
# DATABASE (MySQL)
# ========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# ========================
# AUTH SETTINGS
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "users_db.CustomUser"
LOGIN_REDIRECT_URL = "/"


# ========================
# INTERNATIONALIZATION
# ========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True


# ========================
# STATIC FILES (BEST PRACTICES)
# ========================
STATIC_URL = "/static/"

# Folder tempat file static mentah
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Folder hasil collectstatic (JANGAN diubah)
STATIC_ROOT = BASE_DIR / "staticfiles"


# ========================
# MEDIA FILES
# ========================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ========================
# AUTO FIELD
# ========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# XENDIT PAYMENT GATEWAY
XENDIT_SECRET_KEY = config('XENDIT_SECRET_KEY')
XENDIT_PUBLIC_KEY = config('XENDIT_PUBLIC_KEY')
XENDIT_IS_PRODUCTION = config('XENDIT_IS_PRODUCTION', default=False, cast=bool)

# Validate keys
if not XENDIT_SECRET_KEY or not XENDIT_PUBLIC_KEY:
    if XENDIT_IS_PRODUCTION:
        raise ValueError("XENDIT_SECRET_KEY and XENDIT_PUBLIC_KEY must be set in production.")
    else:
        import warnings
        warnings.warn("Xendit keys are not set. Payment integration will fail.")

# ========================
# EMAIL CONFIGURATION 
# ========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '@gmail.com'  # Your sending email
EMAIL_HOST_PASSWORD = 'your_app_password'  # Use app password for Gmail
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'