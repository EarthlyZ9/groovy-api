from rest_framework import mixins, generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from user.models import User, University
from user.serializers import UserSerializer, UniversitySerializer, MiniUniversitySerializer, SimplifiedUserSerializer

# Create your views here.
"""
Two ways to wrap API views
1) @api_view decorator
2) APIView class
"""


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


class UserApiRoot(generics.GenericAPIView):
    name = 'User'

    def get(self, request, *args, **kwargs):
        return Response({
            'users': reverse('user-list', request=request),
            'university': reverse('university-list', request=request),
            })


