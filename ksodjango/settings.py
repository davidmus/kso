DEBUG = False
TEMPLATE_DEBUG = DEBUG
WORKING_OFFLINE = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kso',
        'USER': 'kso',
        'PASSWORD': 'N3dkeene',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = '/Users/david/src/ksohg/ksodjango/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/Users/david/src/ksohg/ksodjango/static'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '%j=$#_7ht5$u#zbkd4sos+tod8h3jdaydqnpaobqzka)93570w'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'ksodjango.urls'

TEMPLATE_DIRS = (
    'templates',
    'kso/views',
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'ksodjango.kso',
    'markitup',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

MARKITUP_SET = 'markitup/sets/markdown'

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''