"""
Django settings for tastyblog project.
Generated by 'django-admin startproject' using Django 3.2.13.
"""

from pathlib import Path
import os
import dj_database_url

# ✅ Load env.py if present (for local secrets)
if os.path.isfile('env.py'):
    import env

# === BASE PATHS ===
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# === SECURITY ===
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-local-secret-key')  # Local fallback
DEBUG = os.environ.get('DEBUG', 'True') == 'True'  # True for local, False in production

X_FRAME_OPTIONS = 'SAMEORIGIN'

ALLOWED_HOSTS = [
    'tasty-blog-portfolio-project-4.herokuapp.com',
    'localhost',
    '127.0.0.1'
]

# === INSTALLED APPS ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'django_summernote',
    'crispy_forms',
    'posts.apps.PostsConfig',
    'books',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = "/profile"
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# === MIDDLEWARE ===
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tastyblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context_processors.extras',
            ],
        },
    },
]

WSGI_APPLICATION = 'tastyblog.wsgi.application'

# === DATABASE CONFIG ===
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# === PASSWORD VALIDATORS ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === INTERNATIONALIZATION ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === STATIC & MEDIA ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

# === CLOUDINARY CONFIG ===
CLOUDINARY_URL = os.environ.get(
    'CLOUDINARY_URL',
    'cloudinary://736832558482829:j7KxZoclb2xsUrgxcHEL0sXmbV0@dzxx8m2el'  # fallback for local
)
os.environ.setdefault('CLOUDINARY_URL', CLOUDINARY_URL)

# Use Cloudinary for media (uploaded user files)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Use WhiteNoise for static files (CSS, JS)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === DEFAULT PK FIELD ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_PROFILE_MODULE = 'posts.Profile'
