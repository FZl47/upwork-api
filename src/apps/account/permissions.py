from rest_framework import permissions


class UserRolePermission(permissions.BasePermission):
    message = 'PermissionDenied: role is not allowed to perform this action'
    role = None

    def __init__(self, role, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous or user.is_authenticated is False:
            return False

        if user.role == self.role:
            return True
        return False

    def __call__(self, *args, **kwargs):
        return self
