import platform
import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

AWS_SECRETS_MANAGER_SECRETS_SECTION = 'mashup:production'

# AWS
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']

DEBUG = False or (
        len(sys.argv) > 1
        and sys.argv[1] == 'runserver'
        and platform.system() != 'Linux'
)
ALLOWED_HOSTS += [
    'localhost',
    'mashup.localhost',
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    'mashup.lhy.kr',
]
DATABASES = SECRETS['DATABASES']
DBBACKUP_STORAGE_OPTIONS['bucket_name'] = SECRETS['AWS_STORAGE_BUCKET_NAME']

# Sentry
sentry_sdk.init(
    dsn=SECRETS['SENTRY_DSN'],
    integrations=[DjangoIntegration()]
)

# WSGI
WSGI_APPLICATION = 'config.wsgi.production.application'


def is_ec2_linux():
    """
    Detect if we are running on an EC2 Linux Instance
    See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        response = urlopen('http://169.254.169.254/latest/meta-data/local-hostname')
        ec2_hostname = response.read().decode('utf-8')
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)
