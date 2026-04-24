from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GameSession
from .serializers import GameSessionSerializer
from .services import spin_game


# Create your views here.
class StartSessionView(APIView):
    """
    Start a new game session for authenticated user.
    
    Allows only one active session per user.
    A New session starts with 10 credits
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
                {"detail": "Active session already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session = GameSession.objects.create(user=user)
        serializer = GameSessionSerializer(session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class SpinView(APIView):
    """
    Execute a spin for the current user's active session.
    
    Returns the spin result including symbols, reward, and updated credits.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Get active session
        session = GameSession.objects.filter(
            user=user,
            is_active=True
        ).first()

        if not session:
            return Response(
                {"detail": "No active session found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            result = spin_game(session)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(result, status=status.HTTP_200_OK)
