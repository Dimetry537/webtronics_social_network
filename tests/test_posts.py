import pytest

import pytest
from tests.conftest import client

def test_create_post():
    response = client.post("/auth/register", json={
        "email": "post@example.com",
        "password": "strings",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    })
    assert response.status_code == 201

    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "post@example.com",
            "password": "strings"
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    access_token = response.json()["access_token"]
    response = client.post(
        "/user/posts/",
        json={
            "content": "test content"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["content"] == "test content"


def test_view_all_posts():
    response = client.get("/user/posts/")
    assert response.status_code == 200

def test_update_post():
    create_response = client.post(
        "/user/posts/",
        json={
            "title": "test title",
            "content": "test content"
        }
    )
    update_response = client.patch(
        f"/user/posts/{create_response.json()['id']}",
        json={
            "title": "updated title"
        }
    )
    assert update_response.json()["title"] == "updated title"

def test_delete_post():
    create_response = client.post(
        "/user/posts/",
        json={
            "title": "test title",
            "content": "test content"
        }
    )
    delete_response = client.delete(f"/user/posts/{create_response.json()['id']}")
    assert delete_response.status_code == 200

def test_post_not_found():
    response = client.get("/user/posts/999")
    assert response.status_code == 405