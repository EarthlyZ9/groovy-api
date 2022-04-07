from django.http import JsonResponse
from rest_framework import generics, status, filters
from rest_framework.response import Response

from friend.models import Friend, FriendRequest
from friend.serializers import FriendSerializer, FriendRequestSerializer
from friend.services import FriendService
from user.models import User
from user.serializers import SimplifiedUserSerializer
from user.services import NotificationService


class FriendList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SimplifiedUserSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset()
        friends = self.serializer_class(queryset.filter(friend_user=user).all(), many=True).data
        friend_request_count = FriendService.count_friend_request(user)
        latest_request = FriendService.get_latest_friend_request(user)
        return JsonResponse({'friends': friends,
                             'latest_request': latest_request,
                             'friend_request_count': friend_request_count},
                            safe=False, status=status.HTTP_200_OK)


class FriendDetail(generics.RetrieveDestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data['friend'])


class FriendRequestList(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(request_to=user).all()


class FriendRequestDetail(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer


class UserSearch(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SimplifiedUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname"]


class SendFriendRequest(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        request_from = request.user
        request_to_id = kwargs.get("pk")
        request_to = User.objects.get(pk=request_to_id)

        friend_request, sent = FriendService.send_friend_request(request_from, request_to)
        NotificationService.notify_friend_request(request_from, request_to)

        if sent:
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
