import glob
import os

from configurations import Configuration, values
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseConfiguration(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

    #Django environ
    #FIXME: we must have oportunity upload settings from env file
    #DOTENV = os.path.join(BASE_DIR, '.env')

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.Value(
        '3@a)-cbt514^!a%qiotx$su4%29p@dxfrd-qb(oouzbp^@!+gr', environ_prefix=''
    )

    #FIXME: we must setup that list
    ALLOWED_HOSTS = ['*']


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_celery_beat',
        'django_celery_results',
        'rest_framework',

        'scheduler.api',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'scheduler.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    WSGI_APPLICATION = 'scheduler.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://scheduler:scheduler@scheduler_postgres/scheduler'
        )
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    TROOD_AUTH_SERVICE_URL = values.URLValue(
        'http://authorization.trood:8000/', environ_prefix=''
    )

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'trood_auth_client.authentication.TroodTokenAuthentication',
        ),
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                        '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'WARNING',  # To capture more than ERROR, change to WARNING, INFO, etc.
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    # FIXME: must be setupable
    RAVEN_CONFIG = {
        'dsn': 'http://4d8d2a23c26a4a9e8c44f9f4b9c3b3d5:6a34464e42ca41c58ff424a3c821f50f@sentry.dev.trood.ru/7',
        'release': 'dev'
    }

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

    # Celery configuration
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html

    CELERY_BROKER_URL = values.Value('RABBITMQ_URL', envron_prefix='')

    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_TASK_SERIALIZER = 'json'

    CELERY_IMPORTS = [module[:-3].replace("/", ".") for module in glob.glob('tasks/*.py')]


    SERVICE_DOMAIN = values.Value('', environ_prefix='')
    SERVICE_AUTH_SECRET = values.Value('', environ_prefix='')


    CUSTODIAN_URL = values.URLValue('http://custodian.trood:8000/custodian/', environ_prefix='')
    MAIL_SERVICE_URL = values.URLValue('http://mail.trood:8000', environ_prefix='')
    SYSTEM_MAIL_ID = values.IntegerValue(1, environ_prefix='')

class Development(BaseConfiguration):
    DEBUG = True

class Production(BaseConfiguration):
    DEBUG = False