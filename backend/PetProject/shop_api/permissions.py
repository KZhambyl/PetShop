from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Allow read to anyone, but write only to the review owner.

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner
        return obj.user == request.user


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    # Allow read to all, delete to admins or owner.

    def has_object_permission(self, request, view, obj):
        # Everyone can read
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only owner or admin can write/delete
        return obj.user == request.user or request.user.is_staff
    
class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_authenticated and request.user.is_staff
        )
