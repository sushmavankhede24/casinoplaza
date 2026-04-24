from django.db import models
from django.conf import settings
# Create your models here.

class GameSession(models.Model):
    """
    Represents a game session for a user.

    Each session starts with fixed credits and ends
    when user cashes out or credits reach zero.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    credits = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.user.username}"