from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GameSession
from .serializers import GameSessionSerializer
from .services import spin_game, cashout_session


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


class CashoutView(APIView):
    """
    Cash out the current user's active session.

    Transfers remaining session credits to the user's wallet
    and marks the session as inactive.
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
            result = cashout_session(session)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(result, status=status.HTTP_200_OK)
    

class GameStatusView(APIView):
    """
    Retrieve the current game status for the authenticated user.

    Returns current session credits, wallet balance,
    and whether an active session exists.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get active session (if any)
        session = GameSession.objects.filter(
            user=user,
            is_active=True
        ).first()

        return Response(
            {
                "credits": session.credits if session else 0,
                "wallet_balance": user.wallet_balance,
                "is_active": bool(session),
            },
            status=status.HTTP_200_OK
        )