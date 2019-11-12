from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'


class DBStorage(S3Boto3Storage):
    location = 'db'
    default_acl = 'private'
