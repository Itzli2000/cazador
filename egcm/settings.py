import os

from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '=mg-a&h-2_v83di84*8a)=8(56rp-pm52$w@t+a8-i)j$se917'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0',
    '127.0.0.1',
    'localhost',
    'egcm.giovannicortes.com', 
    'elgrancazadormexico.com.mx',
]

URL_DOMAIN = os.environ.get('URL_DOMAIN')

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # vendors apps
    'tinymce',
    'paypal.standard.ipn',

    # egcm apps
    'accounts.apps.AccountsConfig',
    'shop.apps.ShopConfig',
    'restaurant.apps.RestaurantConfig',
    'blog.apps.BlogConfig',
    'menues.apps.MenuesConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'contact.apps.ContactConfig',
    'payment.apps.PaymentConfig',
    'flatcustom',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'egcm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'egcm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Email settings
EMAIL_TEMPLATE_ROOT = os.path.join(BASE_DIR, 'static', 'mail')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 25
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Accounts
AUTH_USER_MODEL = 'accounts.User'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Session
CART_SESSION_ID = 'cart'

# TinyMCE

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Conekta
CONEKTA_API_KEY = os.environ.get('CONEKTA_API_KEY')

# Paypal
PAYPAL_RECEIVER_EMAIL = "g-facilitator@giovannicortes.com"
PAYPAL_TEST = True
