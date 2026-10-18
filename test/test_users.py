from jose import jwt

from app import oauth2, schemas


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_user(client):
    res = client.post("/api/v1/users/", json={"email": "hello1234@gmail.com", "password": "password123"})
    new_user = schemas.User(**res.json())
    assert new_user.email == "hello1234@gmail.com"
    assert res.status_code == 201


def test_get_user(client):
    created = client.post("/api/v1/users/", json={"email": "hello1234@gmail.com", "password": "password123"})
    new_user = schemas.User(**created.json())

    res = client.get(f"/api/v1/users/{new_user.id}")
    user = schemas.User(**res.json())
    assert user.id == new_user.id
    assert user.email == new_user.email
    assert res.status_code == 201


def test_get_user_not_found(client):
    res = client.get("/api/v1/users/99999")
    assert res.status_code == 404


def test_login_user(client, test_user):
    res = client.post(
        "/api/v1/auth/login/",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, oauth2.SECRET_KEY, algorithms=[oauth2.ALGORITHM])
    assert res.status_code == 200
    assert login_res.token_type == "bearer"
    assert payload.get("user_id") == test_user["id"]


def test_incorrect_login(client, test_user):
    res = client.post(
        "/api/v1/auth/login/",
        data={"username": test_user["email"], "password": "wrongpassword"},
    )
    assert res.status_code == 403
    assert res.json().get("detail") == "Invalid Credentials"
