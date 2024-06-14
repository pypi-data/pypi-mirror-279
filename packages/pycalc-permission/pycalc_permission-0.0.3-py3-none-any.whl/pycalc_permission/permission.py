from rest_framework.permissions import BasePermission
from rest_framework import exceptions


class IsAccessAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # print('user ==', request.user)
        # print('auth ==', request.auth)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print('has_object_permission ==')
        print(request.method, request.user)
        print(obj)
        return True


class ModelPermission(IsAccessAuthenticated):
    permissions = {}

    def has_object_permission(self, request, view, obj):
        roles = self.permissions.get(request.method)
        if roles is None:
            raise exceptions.MethodNotAllowed(request.method)

        print(request.user.roles)
        print(roles)
        return request.user.contain(roles)
