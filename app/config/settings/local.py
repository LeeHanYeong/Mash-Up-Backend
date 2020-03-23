from .dev import *

AWS_SECRETS_MANAGER_SECRET_SECTION = 'mashup:dev'

DATABASES['default']['HOST'] = 'localhost'
