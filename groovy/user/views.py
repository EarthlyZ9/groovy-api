from rest_framework import generics
from user.models import User, University
from user.serializers import (
    UserSerializer,
    UniversitySerializer,
    MiniUniversitySerializer,
)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UniversityList(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = MiniUniversitySerializer


class UniversityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

