"""root url configurations and version routers"""
from django.urls import re_path, include


urlpatterns = [
    re_path(r"^api/v1/", include("config.urls_v1")),
]
