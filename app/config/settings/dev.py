from .base import *

AWS_SECRETS_MANAGER_SECRET_SECTION = 'mashup:dev'

DEBUG = True
ALLOWED_HOSTS += [
    '*',
]

# AWS
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']

# DB
DATABASES = SECRETS['DATABASES']
DBBACKUP_STORAGE_OPTIONS['bucket_name'] = SECRETS['AWS_STORAGE_BUCKET_NAME']

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
