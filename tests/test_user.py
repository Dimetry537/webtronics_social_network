import pytest

from tests.conftest import client
from src.models import *


def test_register():
    response = client.post("/auth/register", json={
          "email": "user@example.com",
          "password": "strings",
          "is_active": True,
          "is_superuser": False,
          "is_verified": False,
    })

    assert response.status_code == 201

def test_register_same_email():
    response = client.post("/auth/register", json={
          "email": "user@example.com",
          "password": "strings",
          "is_active": True,
          "is_superuser": False,
          "is_verified": False,
    })

    assert response.status_code == 400

def test_authenticate_true():
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "user@example.com",
            "password": "strings"
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_authenticate_wrong_username():
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "wrong@example.com",
            "password": "strings"
        },
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'LOGIN_BAD_CREDENTIALS'

def test_authenticate_wrong_password():
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "user@example.com",
            "password": "wrong_password"
        },
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'LOGIN_BAD_CREDENTIALS'
