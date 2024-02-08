from fastapi import Response
from .conftest import client
from httpx import Response
from httpx import AsyncClient

async def test_signup(ac: AsyncClient):
    resp = await ac.post("/users/signup", json={"username": "user", "first_name": "user", "last_name": "user",
                                             "password": "123"})
    data = resp.json()
    assert resp.status_code == 201
    assert data['username'] == "user"

async def test_user(logged_in_client: AsyncClient):
    resp = await logged_in_client.get("/users/me")
    data = resp.json()
    assert resp.status_code == 200

async def test_login(ac: AsyncClient):
    user_data = {"username": "user", "first_name": "user", "last_name": "user",
                                             "password": "123"}
    resp = await ac.post("/users/signup", json=user_data)
    resp = await ac.post("/auth/token", data={"username": "user",
                                              "password": "123"})
    
    assert resp.status_code == 200
    assert resp.json().get("access_token")


async def test_signup_with_existing_username(ac: AsyncClient):
    resp = await ac.post("/users/signup", json={"username": "doc", "first_name": "doc", "last_name": "doc",
                                             "password": "123"})
    assert resp.status_code == 201
    resp = await ac.post("/users/signup", json={"username": "doc", "first_name": "doc1", "last_name": "doc",
                                             "password": "123"})
    assert resp.status_code == 400

async def test_signup_with_existing_email(ac: AsyncClient):
    resp = await ac.post("/users/signup", json={"username": "doc", "email": "example@mail.ru", 
                                                          "first_name": "doc", "last_name": "doc",
                                                          "password": "123"})
    assert resp.status_code == 201
    resp = await ac.post("/users/signup", json={"username": "doc1", "email": "example@mail.ru",
                                                          "first_name": "doc1", "last_name": "doc",
                                                          "password": "123"})
    assert resp.status_code == 400