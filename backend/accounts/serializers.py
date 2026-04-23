from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration.
    
    Handles validation and creation of new users.
    Ensures password is write-only and securely stored using Django's hashing.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password"]


    def create(self, validated_data):
        """
        Create a new user using Django's build-in create_user method

        This ensures:
        - password is hashed
        - User is created securely
        """
        return User.objects.create_user(**validated_data)