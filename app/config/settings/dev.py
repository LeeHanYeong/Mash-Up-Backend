from .base import *

import_secrets()

DEBUG = True
ALLOWED_HOSTS += [
    'mashup.localhost',
    'localhost',
    '127.0.0.1',
]

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
