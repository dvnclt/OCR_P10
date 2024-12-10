from rest_framework import serializers

from .models import Project, Contributor, Issue
from User.serializers import SimplifiedUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    author = SimplifiedUserSerializer(required=False)
    contributors_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'author', 'type', 'created_at',
            'updated_at', 'contributors_count'
            ]
        read_only_fields = [
            'created_at', 'updated_at'
            ]

    def get_contributors_count(self, obj):
        return obj.contributors.count()


class SimplifiedProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class ContributorSerializer(serializers.ModelSerializer):
    contributor_id = serializers.ReadOnlyField(source='id')
    user = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'contributor_id', 'user', 'role', 'date_joined'
        ]
        read_only_fields = ['date_joined']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'author',
                  'assigned_to', 'priority', 'tag', 'status', 'created_at',
                  'updated_at'
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
