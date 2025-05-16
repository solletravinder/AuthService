import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app

client = TestClient(app)

def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_register_not_implemented():
    data = {"email": "test@example.com", "password": "password123", "full_name": "Test User"}
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 501

def test_login_invalid_credentials():
    resp = client.post("/auth/login", data={"username": "nouser", "password": "wrong"})
    assert resp.status_code == 401

def test_logout():
    resp = client.post("/auth/logout")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Successfully logged out"

def test_oauth_start_invalid_provider():
    resp = client.get("/auth/oauth/unknown")
    assert resp.status_code == 500 or resp.status_code == 501

def test_oauth_callback_invalid_state():
    resp = client.get("/auth/oauth/google/callback?code=abc&state=invalid")
    assert resp.status_code == 400

def test_users_me_unauthorized():
    resp = client.get("/users/me")
    assert resp.status_code == 403 or resp.status_code == 401
