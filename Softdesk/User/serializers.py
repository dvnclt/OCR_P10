from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'date_joined', 'can_be_contacted',
            'can_data_be_shared', 'is_active', 'last_login', 'is_staff',
            'is_superuser'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'is_staff', 'is_active',
            'is_superuser', 'password'
            ]

    def validate_date_of_birth(self, value):
        user = User(date_of_birth=value)
        if not user.is_of_age(min_age=15):
            raise serializers.ValidationError(
                "Inscription refusée, l'âge minimum est de 15 ans"
            )
        return value
