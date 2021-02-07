from rest_framework.permissions import BasePermission


class IsMeOrReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method == 'GET':
            return True
        else:
            return bool(request.user.is_authenticated and request.user.username == 'juanb')

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == 'GET':
            return True
        else:
            return bool(request.user.is_authenticated and request.user.username == 'juanb')