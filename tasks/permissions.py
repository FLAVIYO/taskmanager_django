from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admins or the task owner to perform actions
        return request.user.role == 'ADMIN' or obj.user == request.user