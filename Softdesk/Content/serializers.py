from rest_framework import serializers
from .models import Project, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'author', 'created_at', 'updated_at'
            ]
        read_only_fields = [
            'id', 'author', 'created_at', 'updated_at'
            ]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            'id', 'user', 'project', 'role', 'date_joined'
            ]
        read_only_fields = [
            'id', 'user', 'project', 'date_joined'
            ]
