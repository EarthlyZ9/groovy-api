from rest_framework import generics, status

from config.Response import Response
from friend.models import Friend, FriendRequest
from friend.serializers import FriendSerializer, FriendRequestSerializer
from friend.services import FriendService
from user.models import User
from user.serializers import SimplifiedUserSerializer
from user.services import NotificationService


class FriendList(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SimplifiedUserSerializer

    def get(self, request):
        user = request.user
        queryset = self.get_queryset()
        friends = FriendService.get_all_friends(queryset, user)
        friends_data = self.serializer_class(friends, many=True).data
        return Response(data=friends_data)


class FriendDetail(generics.RetrieveDestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data['friend'])

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        FriendService.delete_friend(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestList(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendService.get_all_friend_request(user=user)


class SendFriendRequest(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        request_from = request.user
        request_to_id = kwargs.get("pk")
        request_to = User.objects.get(pk=request_to_id)

        friend_request, sent = FriendService.send_friend_request(request_from, request_to)
        NotificationService.notify_friend_request(request_from, request_to)

        if sent:
            return Response(data=FriendRequestSerializer(friend_request).data)


class UpdateFriendRequest(generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        changed_status = kwargs.get("status")
        friend_request_obj = self.get_object()
        request_from = friend_request_obj.request_from
        request_to = friend_request_obj.request_to

        updated_friend_request_obj = FriendService.update_friend_request_status(friend_request_obj, changed_status)

        if changed_status == FriendRequest.ACCEPTED:
            FriendService.add_friend(request_from=request_from, request_to=request_to, )
            NotificationService.notify_friend_request_accepted(
                request_from=request_from,
                request_to=request_to,
            )

        return Response(data=FriendRequestSerializer(updated_friend_request_obj).data)
