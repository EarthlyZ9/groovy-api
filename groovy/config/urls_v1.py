"""root url configurations and routers for version 1"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

# API docs
api_info = openapi.Info(
    title="CODOT - Groovy API",
    default_version="v1",
    description="CODOT - Groovy Application을 위한 API 문서",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="nsong.lim@gmail.com"),
    license=openapi.License(name="BSD License"),
)
SchemaView = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Admin page
admin.site.site_header = "커닷 관리자 페이지"
admin.site.site_title = "커닷 관리자 페이지"
admin.site.site_url = "/"
admin.site.index_title = "서비스 관리"
admin.site.empty_value_display = "비어있음"

# url configuration
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("group/", include("group.urls")),
    path("user/", include("user.urls")),
    path("chat/", include("chat.urls")),
    path("friend/", include("friend.urls")),
]

urlpatterns += [
    re_path(
        r"^docs/$",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
