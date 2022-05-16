from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
        is_university_email = request.data.get("is_university_email")

        if not all((email, password)):
            raise exceptions.ParseError("invalid input form given")

        if User.objects.filter(email=email).exists():
            return Response(data="이미 가입된 이메일입니다.", status=status.HTTP_409_CONFLICT)

        is_university_confirmed = False
        university_confirmed_at = None

        if is_university_email:
            is_university_confirmed = True
            university_confirmed_at = datetime.now()

        user = User.objects.create_user(
            email=email,
            password=password,
            nickname=nickname,
            is_univerisity_email=is_university_email,
            is_university_confirmed=is_university_confirmed,
            university_confirmed_at=university_confirmed_at,
        )

        token = get_tokens_for_user(user)  # {refresh, access}
        serializer = UserSerializer(user)

        return Response(data=dict(user=serializer.data, token=token))


class EmailVerification(APIView):
    """
    유효한 이메일인지 확인하기 위해 이메일 전송
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user_email = request.data.get("email")
        subject = '[Groovy] 회원가입 인증 메일입니다.'
        message = {'uid': urlsafe_base64_encode(force_bytes(user_email))}
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user_email])

        return Response(data=dict(email=user_email, message=message))


class VerifyEmail(APIView):

    def post(self, request, *args, **kwargs):
        uid64 = request.data.get("uid64")
        email = force_str(urlsafe_base64_decode(uid64))
        return Response(data=email)


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
        # TODO: soft delete user
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
