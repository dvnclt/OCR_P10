from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import User
from .serializers import UserSerializer
from Content.serializers import SimplifiedProjectSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()

    def perform_update(self, serializer):
        if self.request.user == self.get_object() or self.request.user.is_staff:  # noqa:E501
            serializer.save()
        else:
            raise PermissionDenied("Accès refusé")

    def perform_destroy(self, instance):
        self.object = self.get_object()
        if self.object == self.request.user or self.request.user.is_staff:
            self.object.delete()
        else:
            raise PermissionDenied("Accès refusé")

    @action(detail=True, methods=['get'], url_path='projects')
    def get_user_authored_projects(self, request, pk=None):
        # Filtre les projets par auteur (user)
        user = self.get_object()
        projects = user.authored_projects.all()
        serializer = SimplifiedProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
