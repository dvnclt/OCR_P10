from rest_framework import viewsets, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectSerializer, ContributorSerializer,
                          IssueSerializer, CommentSerializer)


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

    def perform_update(self, serializer):
        project = self.get_object()
        if project.author != self.request.user:
            raise PermissionDenied("Accès refusé")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Accès refusé")
        instance.delete()

    # Action personnalisée pour lister les contributeurs d'un projet
    @action(detail=True, methods=['get'], url_path='contributors')
    def get_contributors_for_project(self, request, pk=None):
        project = self.get_object()
        contributors = project.contributors.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Action personnalisée pour lister les issues d'un projet
    @action(detail=True, methods=['get'], url_path='issues')
    def get_issues_for_project(self, request, pk=None):
        project = self.get_object()
        issues = project.issues.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Action personnalisée pour les détails d'une issue spécifique
    @action(detail=True, methods=['get'],
            url_path='issues/(?P<issue_id>[^/.]+)')
    def get_issue_details(self, request, pk=None, issue_id=None):
        try:
            # Récupère le projet
            project = self.get_object()
            # Récupère l'issue via son id
            issue = project.issues.get(id=issue_id)

            # Sérialise et retourne les détails de l'issue
            serializer = IssueSerializer(issue)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Issue.DoesNotExist:
            # Si l'issue n'existe pas ou n'appartient pas au projet
            return Response(
                {"detail": "Aucune issue disponible."},
                status=status.HTTP_404_NOT_FOUND
            )

    # Action personnalisée pour lister les comments d'une issue d'un projet
    @action(detail=True, methods=['get'],
            url_path='issues/(?P<issue_id>[^/.]+)/comments')
    def get_comments_for_issue(self, request, pk=None, issue_id=None):
        try:
            project = self.get_object()
            issue = project.issues.get(id=issue_id)
            # Récupère l'ensemble des commentaire pour l'issue donnée
            comments = issue.comments.all()

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Issue.DoesNotExist:
            return Response(
                {"detail": "Aucun commentaire disponible."},
                status=status.HTTP_404_NOT_FOUND
            )


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

        # Vérifie si le contributeur fait partie du projet
        if Contributor.objects.filter(user=user, project=project).exists():
            serializer.save(author=user)
        else:
            raise PermissionDenied("Accès refusé")

    def perform_update(self, serializer):
        issue = self.get_object()

        # Vérifie si l'utilisateur est l'auteur de l'issue
        if issue.author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("Accès refusé.")

    def perform_destroy(self, instance):
        # Vérifie si l'utilisateur est l'auteur de l'issue
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("Accès refusé.")

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments_for_issue(self, request, pk=None):
        issue = self.get_object()
        comments = issue.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        issue = serializer.validated_data['issue']
        project = issue.project

        # Vérifie si l'issue existe
        if not Issue.objects.filter(id=issue.id).exists():
            raise PermissionDenied("Cette issue n'existe pas.")

        # Vérifie si le contributeur fait partie du projet
        if Contributor.objects.filter(user=user, project=project).exists():
            serializer.save(author=user)
        else:
            raise PermissionDenied("Accès refusé")

    def perform_update(self, serializer):
        comment = self.get_object()
        # Vérifie si l'utilisateur est l'auteur du commentaire
        if comment.author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("Accès refusé")

    def perform_destroy(self, instance):
        # Vérifie si l'utilisateur est l'auteur du commentaire
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("Accès refusé")
