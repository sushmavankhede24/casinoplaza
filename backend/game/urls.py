from django.urls import path
from .views import StartSessionView

urlpatterns = [
    path("start-session/", StartSessionView.as_view()),
]