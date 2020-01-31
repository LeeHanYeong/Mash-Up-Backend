from .base import *

AWS_SECRETS_MANAGER_SECRET_SECTION = 'mashup:dev'

DEBUG = True
ALLOWED_HOSTS += [
    'mashup.localhost',
    'localhost',
    '127.0.0.1',
]

# AWS
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']

# DB
DATABASES = SECRETS['DATABASES']
DBBACKUP_STORAGE_OPTIONS['bucket_name'] = SECRETS['AWS_STORAGE_BUCKET_NAME']

# django-push-notifications
# PUSH_NOTIFICATIONS_SETTINGS['FCM_API_KEY'] = SECRETS['FCM_API_KEY']

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
