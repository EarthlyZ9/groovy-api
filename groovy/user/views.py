from rest_framework import generics, filters, mixins

from config.Response import Response
from user.models import User, University, UniversityManualVerification
from user.serializers import (
    UserSerializer,
    UniversitySerializer,
    MiniUniversitySerializer, UniversityVerificationSerializer,
)
from user.services import UserService


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname"]


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UniversityList(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = MiniUniversitySerializer


class UniversityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class UniversityVerification(generics.CreateAPIView, mixins.RetrieveModelMixin):
    """
    Manual Verification for those no school email address
    """
    queryset = UniversityManualVerification.objects.all()
    serializer_class = UniversityVerificationSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = UserService.get_university_verification_request(user)
        serializer = self.get_serializer(instance)

        return Response(data=serializer.data)
