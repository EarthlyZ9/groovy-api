from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

from . import auth_views

urlpatterns = [
    path(
        "check-email/",
        auth_views.CheckDuplicateUsernameView.as_view(),
        name="check-email",
    ),
    path("verify-email/", auth_views.EmailVerification.as_view(), name="verify-email"),
    path('verify-email/<str:uid64>/', auth_views.VerifyEmail.as_view(), name="activate"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password-change",
    ),
    path(
        "service-term/",
        auth_views.TermAgreementView.as_view(),
        name="service-term-agreement",
    ),
]
urlpatterns += [
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
urlpatterns += [
    path("basic/signup/", auth_views.BasicSignUpView.as_view(), name="basic-signup"),
    path("basic/signin/", auth_views.BasicSignInView.as_view(), name="basic-signin"),
    path("basic/leave/", auth_views.SecessionView.as_view(), name="basic-leave"),
]
