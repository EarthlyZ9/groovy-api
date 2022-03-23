from rest_framework import generics
from friend.models import Friend, FriendRequest
from friend.serializers import FriendSerializer, FriendRequestSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response


class FriendApiRoot(generics.GenericAPIView):
    name = 'Friend'

    def get(self, request, *args, **kwargs):
        return Response({
            'friend': reverse('friend-list', request=request),
            'friend_request': reverse('friend-request-list', request=request),
            })


class FriendList(generics.ListCreateAPIView):
    queryset = Friend.objects.all().order_by('user_id')
    serializer_class = FriendSerializer


class FriendDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


class FriendRequestList(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all().order_by('request_from')
    serializer_class = FriendRequestSerializer


class FriendRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
