"""
Django settings for music_dashboard project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os, sys
from pathlib import Path
import dotenv
import graypy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok = True)

GRAYLOG_HOST = 'graylog'
GRAYLOG_PORT = 12201

docker_env = os.getenv('DOCKER_ENV', 'false')
if docker_env == 'true':
    dotenv.read_dotenv('.env.docker')
else:
    print('using local setting')
    dotenv.read_dotenv('.env.local')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s9j78j9!+i)&uh_%wxfxp9wr_h+=pl2-uw!+#i4(vkw-s0f2he"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'


MEDIA_URL='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # 프로젝트의 static 폴더 경로
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic 명령으로 모아질 경로
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Application definition

INSTALLED_APPS = [
    "user_messages.apps.UserMessagesConfig",
    "users.apps.UsersConfig",
    "musics.apps.MusicsConfig",
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    'corsheaders',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.naver",
    "allauth.socialaccount.providers.google",
    "django_prometheus"
]

CORS_ALLOWED_ORIGINS = ['http://localhost:5173']

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "music_dashboard.urls"

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

WSGI_APPLICATION = "music_dashboard.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        # "NAME": BASE_DIR / "db.sqlite3",
        "NAME": os.getenv('MYSQL_DATABASE', 'muze'),
        "USER": os.getenv('MYSQL_USER', 'silver'),
        "PASSWORD": os.getenv('MYSQL_PASSWORD', 'dmstjd6918'),
        "HOST": os.getenv('DB_HOST', '127.0.0.1'),
        "PORT": os.getenv('DB_PORT', 3306),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": 'utf8mb4',
            'connect_timeout': 10,
        }
    }
}

# TEST환경에서만 sqlite3 사용.
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
            'default':{
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory'
            }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'users.User'

INTERNAL_IPS = [
    "127.0.0.1"
]

# oauth setting
SITE_ID = 1

GITHUB_OAUTH_CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID")
GITHUB_OAUTH_CLIENT_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET")

NAVER_OAUTH_CLIENT_ID = os.getenv("NAVER_OAUTH_CLIENT_ID")
NAVER_OAUTH_CLIENT_SECRET = os.getenv("NAVER_OAUTH_CLIENT_SECRET")

GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': GITHUB_OAUTH_CLIENT_ID,
            'secret': GITHUB_OAUTH_CLIENT_SECRET,
            'key': '',
        }
    },
    'naver': {
        'APP':{
            'client_id': NAVER_OAUTH_CLIENT_ID,
            'secret': NAVER_OAUTH_CLIENT_SECRET,
            'key': ''
        }
    },
    'google' : {
        'APP':{
            'client_id': GOOGLE_OAUTH_CLIENT_ID,
            'secret': GOOGLE_OAUTH_CLIENT_SECRET,
            'key': ''
        }
    }
}

SOCIAL_AUTH_GITHUB_REDIRECT_URI = 'http://localhost:8000/accounts/github/login/callback/'  # 로컬 개발 시
SOCIAL_AUTH_NAVER_REDIRECT_URI = 'http://localhost:8000/accounts/naver/login/callback/'  # 로컬 개발 시
SOCIAL_AUTH_GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/google/login/callback/'  # 로컬 개발 시

ACCOUNT_FORMS = {
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'confirm_login_code': 'allauth.account.forms.ConfirmLoginCodeForm',
    'login': 'allauth.account.forms.LoginForm',
    'request_login_code': 'allauth.account.forms.RequestLoginCodeForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'signup': 'allauth.account.forms.SignupForm',
    'user_token': 'allauth.account.forms.UserTokenForm',
}

ACCOUNT_USERNAME_REQUIRED = True
LOGIN_REDIRECT_URL = '/'  # 로그인 후 리다이렉트될 URL
LOGOUT_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level' : 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'muse.log',
            'maxBytes': 1024 * 1024 * 5, # 5MB
            'backupCount': 5,
            'formatter': 'standard'
        },
        'graylog': {
            'level': 'INFO',
            'class': 'graypy.GELFHandler',
            'host': GRAYLOG_HOST,
            'port': GRAYLOG_PORT
        }
    },
    'loggers': {
        'django': {
            'handlers': ['graylog', 'console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'allauth':{
            'handlers': ['graylog', 'console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'user_message':{
            'handlers': ['graylog', 'console', 'file'],
            'level': 'INFO'
        }
    }
}


# CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'