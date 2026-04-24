from django.urls import path
from .views import StartSessionView, SpinView

urlpatterns = [
    path("start-session/", StartSessionView.as_view()),
    path("spin/", SpinView.as_view(), name="spin"),
]