from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'password', 'email', 'first_name',
            'last_name', 'date_of_birth', 'date_joined', 'can_be_contacted',
            'can_data_be_shared', 'is_active', 'last_login', 'is_staff',
            'is_superuser'
        ]
        read_only_fields = [
            'date_joined', 'last_login', 'is_staff', 'is_active',
            'is_superuser'
            ]

    def validate_date_of_birth(self, value):
        user = User(date_of_birth=value)
        if not user.is_of_age(min_age=15):
            raise serializers.ValidationError(
                "Inscription refusée, l'âge minimum est de 15 ans"
            )
        return value


class SimplifiedUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email']
