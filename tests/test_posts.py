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

    post_id = response.json()["id"]
    print(f"Created post with id: {post_id}")


def test_view_all_posts():
    response = client.get("/user/posts/")
    assert response.status_code == 200

def test_update_post():
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

    create_response = client.post(
        "/user/posts/",
        json={
            "content": "test content"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    update_response = client.patch(
        f"/user/posts/{post_id}",
        json={
            "content": "updated title"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["content"] == "updated title"

def test_delete_post():
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

    create_response = client.post(
        "/user/posts/",
        json={
            "content": "test content"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert create_response.status_code == 200
    post_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/user/posts/{post_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert delete_response.status_code == 200


def test_post_not_found():
    response = client.get("/user/posts/999")
    assert response.status_code == 405