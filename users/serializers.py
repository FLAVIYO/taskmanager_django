from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'role']  # Include 'role' if you need it
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Default the role to 'USER' for new users
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'USER')  # Ensure role is set, default is 'USER'
        )
        return user
