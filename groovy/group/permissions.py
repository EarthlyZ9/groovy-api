from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.manager == request.user


class ManagerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return obj.manager == request.user
        else:
            # Check permissions for write request
            return obj.manager == request.user


class IsBookmarkOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        else:
            return obj.user == request.user

