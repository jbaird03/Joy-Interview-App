import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_get_emails():
    with patch("app.email_store.load_emails", return_value=[{"id": "1", "from": "a@example.com", "patient_name": "Jane", "subject": "Hi", "body": "Something", "reply": None}]):
        response = client.get("/emails")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_suggest_reply():
    mock_openai_response = MagicMock()
    mock_openai_response.choices = [MagicMock(message=MagicMock(content="Mocked reply"))]

    with patch("app.main.client.chat.completions.create", return_value=mock_openai_response):
        payload = {"body": "I have a headache", "patient_name": "Jane"}
        response = client.post("/suggest", json=payload)
        assert response.status_code == 200
        assert "suggested" in response.json()
        assert response.json()["suggested"] == "Mocked reply"


def test_send_email_success():
    email_payload = {
        "id": "1",
        "from": "patient@example.com",
        "patient_name": "Jane",
        "subject": "Headache",
        "body": "I have a headache",
        "reply": "Please take ibuprofen."
    }

    with patch("app.main.append_to_sent") as mock_append:
        response = client.post("/send", json=email_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["emailId"] == "1"
        mock_append.assert_called_once()


def test_send_email_missing_reply():
    email_payload = {
        "id": "1",
        "from": "patient@example.com",
        "patient_name": "Jane",
        "subject": "Headache",
        "body": "I have a headache"
    }

    response = client.post("/send", json=email_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Reply is required to send an email."
