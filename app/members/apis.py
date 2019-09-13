from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .filters import UserFilterSet


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
