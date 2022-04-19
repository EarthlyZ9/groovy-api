from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import (
    permissions,
    serializers,
    exceptions,
    status,
    generics,
    mixins,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from config.Response import Response
from .serializers import UserSerializer
from .services import UserService, get_tokens_for_user

User = get_user_model()


class BasicSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        email = request.data.get("email")
        password = request.data.get("password")
        nickname = request.data.get("nickname")
        gender = request.data.get("gender")
        birth_date = request.data.get("birth_date")
        university = request.data.get("university")
        admission_class = request.data.get("admission_class")
        grade = request.data.get("grade")

        if not all((email, password)):
            raise exceptions.ParseError("invalid input form given")

        if User.objects.filter(email=email).exists():
            return Response(data="이미 가입된 이메일입니다.", status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(
            email=email,
            password=password,
            nickname=nickname,
            gender=gender,
            birth_date=birth_date,
            university=university,
            admission_class=admission_class,
            grade=grade,
        )

        token = get_tokens_for_user(user)  # {refresh, access}
        serializer = UserSerializer(user)

        return Response(data=dict(user=serializer.data, token=token))


class EmailVerification(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        # TODO: email verification - sending email
        pass


class BasicSignInView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not all((email, password)):
            raise exceptions.ParseError("invalid input form given")

        user = get_object_or_404(User, email=email)
        if not user.is_deleted:
            raise serializers.ValidationError("비활성화된 계정입니다.")
        elif not check_password(password, user.password):
            raise serializers.ValidationError("잘못된 비밀번호입니다.")

        token = get_tokens_for_user(user)  # {refresh, access}
        serializer = UserSerializer(user)

        return Response(data=dict(user=serializer.data, token=token), status=status.HTTP_200_OK)


class SecessionView(generics.DestroyAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        perform soft delete
        """
        pass

    def update(self, request, *args, **kwargs):
        user = request.user
        reason = request.data.get("deleted_reason", "")
        user_data = UserService.reason_for_leave(user, reason)

        return Response(data=UserSerializer(user_data).data)


class CheckDuplicateUsernameView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            raise serializers.ValidationError("invalid input form")

        if User.objects.filter(email=email).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        if not all((current_password, new_password)):
            raise serializers.ValidationError("invalid input form")

        user = request.user
        if not check_password(current_password, user.password):
            raise serializers.ValidationError("잘못된 비밀번호입니다.")

        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class TermAgreementView(APIView):

    def post(self, request, *args, **kwargs):
        is_service_terms_agreed = request.data.get("is_service_terms_agreed", False)

        user = request.user
        UserService.agree_service_term(user, is_service_terms_agreed)
        return Response(status=status.HTTP_204_NO_CONTENT)
