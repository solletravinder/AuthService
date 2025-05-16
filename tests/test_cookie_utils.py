import os
import pytest
from fastapi import Response

from app.auth.cookie_utils import set_cookie
from config import settings

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv("COOKIE_DOMAIN", raising=False)
    monkeypatch.delenv("COOKIE_SECURE", raising=False)

def test_set_cookie_default(monkeypatch):
    monkeypatch.setattr(settings, "COOKIE_DOMAIN", "")
    response = Response()
    set_cookie(response, "foo", "bar")
    cookie = response.headers.get("set-cookie")
    assert "foo=bar" in cookie
    assert "HttpOnly" in cookie
    assert "Secure" not in cookie
    assert "Domain" not in cookie
    assert "samesite=lax" in cookie.lower()
    # Demonstrate GLOBAL_PATH usage
    assert isinstance(settings.GLOBAL_PATH, str)
    assert settings.GLOBAL_PATH != ""

def test_set_cookie_with_expires(monkeypatch):
    monkeypatch.setattr(settings, "COOKIE_DOMAIN", "")
    response = Response()
    set_cookie(response, "foo", "bar", expires_minutes=10)
    cookie = response.headers.get("set-cookie")
    assert "Expires=" in cookie or "expires=" in cookie

def test_set_cookie_with_domain_localhost(monkeypatch):
    monkeypatch.setattr(settings, "COOKIE_DOMAIN", "localhost")
    response = Response()
    set_cookie(response, "foo", "bar")
    cookie = response.headers.get("set-cookie")
    assert "Domain" not in cookie

def test_set_cookie_with_domain_and_secure(monkeypatch):
    monkeypatch.setattr(settings, "COOKIE_DOMAIN", "example.com")
    monkeypatch.setattr(settings, "COOKIE_SECURE", "True")
    response = Response()
    set_cookie(response, "foo", "bar")
    cookie = response.headers.get("set-cookie")
    assert "Domain=example.com" in cookie
    assert "Secure" in cookie

def test_set_cookie_with_domain_and_insecure(monkeypatch):
    monkeypatch.setattr(settings, "COOKIE_DOMAIN", "example.com")
    monkeypatch.setattr(settings, "COOKIE_SECURE", "False")
    response = Response()
    set_cookie(response, "foo", "bar")
    cookie = response.headers.get("set-cookie")
    assert "Domain=example.com" in cookie
    assert "Secure" not in cookie
