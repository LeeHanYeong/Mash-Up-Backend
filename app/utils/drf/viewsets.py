from rest_framework import mixins
from rest_framework.viewsets import (
    GenericViewSet as DefaultGenericViewSet,
)

__all__ = (
    'GenericViewSet',
    'ListModelViewSet',
    'CreateModelViewSet',
    'RetrieveModelViewSet',
    'UpdateModelViewSet',
    'DestroyModelViewSet',
    'RetrieveUpdateModelViewSet',
    'RetrieveUpdateDestroyModelViewSet',
    'ReadOnlyModelViewSet',
    'ModelViewSet',
)


class GenericViewSet(DefaultGenericViewSet):
    pass


class ListModelViewSet(mixins.ListModelMixin,
                       GenericViewSet):
    pass


class CreateModelViewSet(mixins.CreateModelMixin,
                         GenericViewSet):
    pass


class RetrieveModelViewSet(mixins.RetrieveModelMixin,
                           GenericViewSet):
    pass


class UpdateModelViewSet(mixins.UpdateModelMixin,
                         GenericViewSet):
    pass


class DestroyModelViewSet(mixins.DestroyModelMixin,
                          GenericViewSet):
    pass


class RetrieveUpdateModelViewSet(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 GenericViewSet):
    pass


class RetrieveUpdateDestroyModelViewSet(mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin,
                                        GenericViewSet):
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass
