from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        # Prevent Swagger schema generation from triggering authentication error
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()

        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication credentials were not provided.")
        
        if self.request.user.role == 'ADMIN':
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the task to the logged-in user
        serializer.save(user=self.request.user)
