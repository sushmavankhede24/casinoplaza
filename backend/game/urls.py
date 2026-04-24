from django.urls import path
from .views import StartSessionView, SpinView, CashoutView, GameStatusView

urlpatterns = [
    path("start-session/", StartSessionView.as_view(), name="start-session"),
    path("spin/", SpinView.as_view(), name="spin"),
    path("cashout/", CashoutView.as_view(), name="cashout"),
    path("status/", GameStatusView.as_view(), name="status"),
]