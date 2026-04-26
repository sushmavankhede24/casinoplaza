import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

pytestmark = pytest.mark.django_db

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="test_user", password="test_pass")


def test_login(client, user):
    response = client.post("/api/token/", {
        "username": "test_user",
        "password": "test_pass"
    })

    assert response.status_code == 200
    assert "access" in response.data

def test_start_session(client, user):
    client.force_authenticate(user=user)

    response = client.post("/api/start-session/")
    data = response.data

    assert response.status_code == 201
    assert data["credits"] == 10

def test_spin(client, user):
    client.force_authenticate(user=user)

    client.post("/api/start-session/")
    response = client.post("/api/spin/")

    data = response.data

    assert response.status_code == 200
    assert len(data["symbols"]) == 3

def test_cashout(client, user):
    client.force_authenticate(user=user)

    client.post("/api/start-session/")
    client.post("/api/spin/")

    response = client.post("/api/cashout/")
    data = response.data

    assert response.status_code == 200
    assert "wallet_balance" in data