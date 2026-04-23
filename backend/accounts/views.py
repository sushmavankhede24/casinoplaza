from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    """
    API endpoint for user registration.

    Accepts username and password, validates input,
    and creates a new user in the system.

    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }

    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to register a new user.

        Returns:
            201: User created successfully
            400: Validation errors
        """
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
