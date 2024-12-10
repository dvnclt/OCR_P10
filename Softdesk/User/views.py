from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from Content.serializers import SimplifiedProjectSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()

    @action(detail=True, methods=['get'], url_path='projects')
    def get_user_projects(self, request, pk=None):
        # Filtre les projets par auteur (user)
        user = self.get_object()
        projects = user.authored_projects.all()
        serializer = SimplifiedProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
