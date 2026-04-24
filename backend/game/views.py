from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GameSession
from .serializers import GameSessionSerializer


# Create your views here.
class StartSessionView(APIView):
    """
    Start a new game session.
    
    Rules:
    - User can have only one active session
    - New session starts with 10 credits
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        #Check if active session exists
        active_session = GameSession.objects.filter(
            user=user, is_active=True
        ).first()

        if active_session:
            return Response(
                {"error": "Active session already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session = GameSession.objects.create(user=user)

        serializer = GameSessionSerializer(session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)