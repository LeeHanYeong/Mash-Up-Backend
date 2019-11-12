import os

from aws_secrets import SECRETS

ALLOWED_HOSTS = []

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)

# django-aws-secrets-manager
AWS_SECRETS_MANAGER_SECRETS_NAME = 'lhy'
AWS_SECRETS_MANAGER_PROFILE = 'lhy-secrets-manager'
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'mashup:base'
AWS_SECRETS_MANAGER_REGION_NAME = 'ap-northeast-2'
SECRET_KEY = SECRETS['SECRET_KEY']

# AWS
AWS_S3_ACCESS_KEY_ID = SECRETS['AWS_S3_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = SECRETS['AWS_S3_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = SECRETS['AWS_DEFAULT_ACL']
AWS_BUCKET_ACL = SECRETS['AWS_BUCKET_ACL']
AWS_AUTO_CREATE_BUCKET = SECRETS['AWS_AUTO_CREATE_BUCKET']
AWS_S3_FILE_OVERWRITE = SECRETS['AWS_S3_FILE_OVERWRITE']
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-northeast-2'

# django-dbbackup
DBBACKUP_STORAGE = 'config.storages.DBStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': SECRETS['AWS_S3_ACCESS_KEY_ID'],
    'secret_key': SECRETS['AWS_S3_SECRET_ACCESS_KEY'],
}

# Email
EMAIL_HOST = SECRETS['EMAIL_HOST']
EMAIL_HOST_USER = SECRETS['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = SECRETS['EMAIL_HOST_PASSWORD']
EMAIL_PORT = SECRETS['EMAIL_PORT']
EMAIL_USE_SSL = SECRETS['EMAIL_USE_SSL']
DEFAULT_FROM_EMAIL = SECRETS['DEFAULT_FROM_EMAIL']

# Static
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATICFILES_DIRS = [STATIC_DIR]

# Auth
LOGIN_URL = 'admin:login'
AUTH_USER_MODEL = 'members.User'
ADMIN_USERNAME = 'lhy'
ADMIN_PASSWORD = 'pbkdf2_sha256$120000$9SEp9OZWB5Ya$TVY41qkSk2g5WsPuXXYmYtCh1NwFO5ckJFIyMV8Yi4E='
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.SettingsBackend',
    'members.backends.PhoneNumberBackend',
    'members.backends.EmailBackend',
]

# django-push-notifications
# PUSH_NOTIFICATIONS_SETTINGS = {
#     'WP_PRIVATE_KEY': os.path.join(SECRETS_DIR, 'private_key.pem'),
#     'WP_CLAIMS': {'sub': 'mailto: dev@lhy.kr'},
# }

# django-modeladmin-reorder
ADMIN_REORDER = (
    # 공지
    {'app': 'notice', 'label': '공지사항', 'models': (
        'notice.Notice',
        'notice.Attendance',
    )},
    # 사용자
    {'app': 'members', 'label': '사용자', 'models': (
        'members.UserAdminProxy',
        'members.UserPeriodTeam',
        'members.UserPeriodOutcount',
        # {'model': 'members.UserAdminProxy', 'label': '사용자'},
        # {'model': 'members.UserPeriodTeam', 'label': '사용자 활동기수 정보'},
        # {'model': 'members.UserPeriodOutcount', 'label': '세션'},
    )},
    # 기수, 팀
    {'app': 'members', 'label': '기수 & 팀', 'models': (
        'members.Period',
        'members.Team',
    )},

    'auth',
)

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    'EXCEPTION_HANDLER': 'utils.drf.exceptions.custom_exception_handler',
}

# drf-yasg
BASIC_DESCRIPTION = '''
base64로 인코딩된 사용자ID/비밀번호 쌍을 Header에 전달
HTTP Request의 Header `Authorization`에 
`Basic <base64로 인코딩된 "username:password" 문자열>`값을 넣어 전송
(개발시 일일이 토큰 발급필요없이 편하게 사용 가능)

```
Authorization: Basic ZGVmYXVsdF9jb21wYW55QGxoeS5rcjpkbGdrc2R1ZA==
```
'''
TOKEN_DESCRIPTION = '''
### [DRF AuthToken](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
인증정보를 사용해 [AuthToken](#operation/auth_token_create) API에 요청, 결과로 돌아온 **key**를  
HTTP Request의 Header `Authorization`에 `Token <key>`값을 넣어 전송

```
Authorization: Token fs8943eu342cf79d8933jkd
``` 
'''
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'HTTP Basic Auth(RFC 7617)',
            'description': BASIC_DESCRIPTION,
        },
        'Token': {
            'type': 'DRF AuthToken',
            'description': TOKEN_DESCRIPTION,
        }
    }
}

# Other modules
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# Format
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:M'

# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'KR'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# Application definition
DJANGO_APPS = [
    'members.apps.MembersConfig',
    'notice.apps.NoticeConfig',
    'study.apps.StudyConfig',
    'utils',
]
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'admin_reorder',
    'dbbackup',
    'django_extensions',
    'django_filters',
    'phonenumber_field',
    'push_notifications',
]
DRF_APPS = [
    'drf_yasg',
    'corsheaders',
    'rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_api_key',
]
INSTALLED_APPS = DJANGO_APPS + DEFAULT_APPS + THIRD_PARTY_APPS + DRF_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'admin_reorder.middleware.ModelAdminReorder',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
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

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True
