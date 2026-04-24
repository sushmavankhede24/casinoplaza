from django.urls import path
from .views import StartSessionView, SpinView, CashoutView

urlpatterns = [
    path("start-session/", StartSessionView.as_view(), name="start-session"),
    path("spin/", SpinView.as_view(), name="spin"),
    path("cashout/", CashoutView.as_view(), name="cashout"),
]