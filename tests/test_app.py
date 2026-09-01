import json
import pytest
from pathlib import Path
from starlette.testclient import TestClient

from app.main import app, DATA_FILE


@pytest.fixture(autouse=True)
def clean_subscribers(tmp_path, monkeypatch):
    test_data_file = tmp_path / "subscribers.json"
    test_data_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("app.main.DATA_FILE", test_data_file)
    return test_data_file


@pytest.fixture
def client():
    return TestClient(app)


def test_landing_page_renders_successfully(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "vpublication" in response.text
    assert "vpub" in response.text
    assert "Interactive books, not flat PDFs" in response.text
    assert "vpub-mascot.jpg" in response.text
    assert "hx-post=\"/api/subscribe\"" in response.text
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"


def test_subscribe_success(client, clean_subscribers):
    response = client.post(
        "/api/subscribe",
        data={"email": "author@example.com", "hp_field": ""},
    )
    assert response.status_code == 200
    assert "Welcome" in response.text or "saved your spot" in response.text

    # Verify JSON file has subscriber
    subs = json.loads(clean_subscribers.read_text(encoding="utf-8"))
    assert len(subs) == 1
    assert subs[0]["email"] == "author@example.com"
    assert "subscribed_at" in subs[0]


def test_subscribe_duplicate_email(client, clean_subscribers):
    # First submission
    client.post("/api/subscribe", data={"email": "test@vpub.org", "hp_field": ""})
    
    # Second submission with same email
    response = client.post("/api/subscribe", data={"email": "TEST@vpub.org", "hp_field": ""})
    assert response.status_code == 200
    assert "already on the priority list" in response.text

    # Ensure no duplicate added in JSON
    subs = json.loads(clean_subscribers.read_text(encoding="utf-8"))
    assert len(subs) == 1


def test_subscribe_invalid_email(client, clean_subscribers):
    response = client.post(
        "/api/subscribe",
        data={"email": "not-an-email", "hp_field": ""},
    )
    assert response.status_code == 400
    assert "Please enter a valid email address" in response.text

    # Verify no subscriber added
    subs = json.loads(clean_subscribers.read_text(encoding="utf-8"))
    assert len(subs) == 0


def test_subscribe_honeypot_bot(client, clean_subscribers):
    response = client.post(
        "/api/subscribe",
        data={"email": "bot@spammer.com", "hp_field": "I am a spam bot"},
    )
    assert response.status_code == 200
    # Should not be added to data file
    subs = json.loads(clean_subscribers.read_text(encoding="utf-8"))
    assert len(subs) == 0


def test_404_page(client):
    response = client.get("/non-existent-chapter")
    assert response.status_code == 404
    assert "Page not found" in response.text
    assert "404 Error" in response.text
