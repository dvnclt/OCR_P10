from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment
from User.serializers import SimplifiedUserSerializer
from User.models import User


class ProjectSerializer(serializers.ModelSerializer):
    author = SimplifiedUserSerializer(required=False)
    contributors_count = serializers.SerializerMethodField()
    project_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Project
        fields = [
            'project_id', 'name', 'description', 'author', 'type',
            'created_at', 'updated_at', 'contributors_count'
            ]
        read_only_fields = [
            'created_at', 'updated_at'
            ]

    def get_contributors_count(self, obj):
        return obj.contributors.count()


class SimplifiedProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Project
        fields = ['project_id', 'name', 'description', 'created_at',
                  'updated_at'
                  ]


class ContributorSerializer(serializers.ModelSerializer):
    contributor_id = serializers.IntegerField(source='id', read_only=True)
    user = SimplifiedUserSerializer(read_only=True)  # Sortie
    user_id = serializers.PrimaryKeyRelatedField(  # Entrée
        source='user', queryset=User.objects.all(), write_only=True
    )
    project_id = serializers.PrimaryKeyRelatedField(
        source='project', queryset=Project.objects.all(), write_only=True
    )

    class Meta:
        model = Contributor
        fields = [
            'contributor_id', 'user', 'user_id', 'project_id', 'role',
            'date_joined'
        ]
        read_only_fields = ['date_joined']


class IssueSerializer(serializers.ModelSerializer):
    issue_author = SimplifiedUserSerializer(source='author', required=False,
                                            read_only=True)
    assigned_to = SimplifiedUserSerializer(read_only=True)  # Sortie # noqa: E501
    assigned_to_id = serializers.PrimaryKeyRelatedField(  # Entrée # noqa: E501
        source='assigned_to', queryset=User.objects.all(), write_only=True
    )
    issue_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'description', 'project',
                  'issue_author', 'assigned_to', 'assigned_to_id', 'priority',
                  'tag', 'status', 'created_at', 'updated_at'
                  ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_assigned_to(self, value):
        project_id = self.initial_data.get('project')
        if project_id:
            try:
                project = Project.objects.prefetch_related(
                    'contributors').get(id=project_id)
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    "Le projet spécifié est introuvable."
                    )
            contributors = project.contributors.values_list('user', flat=True)
            if value and value.id not in contributors:
                raise serializers.ValidationError(
                    "Cet utilisateur n'est pas contributeur de ce projet."
                    )
        return value


class SimplifiedIssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Issue
        fields = ['issue_id', 'title']


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source='id', read_only=True)
    issue = SimplifiedIssueSerializer(read_only=True)
    issue_link = serializers.SerializerMethodField()
    issue_id = serializers.PrimaryKeyRelatedField(
        source='issue', queryset=Issue.objects.all(), write_only=True
        )
    comment_author = SimplifiedUserSerializer(source='author', required=False,
                                              read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'content', 'comment_author', 'issue',
                  'issue_link', 'issue_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_issue_link(self, obj):
        return f"http://127.0.0.1:8000/api/issues/{obj.issue.id}/"
