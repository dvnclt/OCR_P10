from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, Contributor, Issue
from .serializers import (ProjectSerializer, ContributorSerializer,
                          IssueSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)

        # Ajoute l'auteur comme étant contributeur
        Contributor.objects.create(
            user=user,
            project=project,
            role='AUTHOR',
            date_joined=project.created_at
        )

    # Action personnalisée pour lister les contributeurs d'un projet
    @action(detail=True, methods=['get'], url_path='contributors')
    def get_contributors(self, request, pk=None):
        project = self.get_object()
        contributors = project.contributors.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Le contributeur actuel crée une issue
        user = self.request.user
        project = serializer.validated_data['project']

        # Vérifie que le contributeur fait partie du projet
        if Contributor.objects.filter(user=user, project=project).exists():
            serializer.save(author=user)
        else:
            raise PermissionDenied("Accès réservé aux contributeurs du projet")

    def perform_update(self, serializer):
        issue = self.get_object()

        # Vérifie que l'utilisateur est l'auteur de l'issue
        if issue.author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("Accès réservé à l'auteur de l'issue.")

    def perform_destroy(self, instance):
        # Vérifie que l'utilisateur est l'auteur de l'issue
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("Accès réservé à l'auteur de l'issue.")
