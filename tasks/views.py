from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication credentials were not provided.")
        
        if self.request.user.role == 'ADMIN':
            return Task.objects.all()
        
        # Return tasks that belong to the authenticated user
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
