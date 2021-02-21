import json
import pytest
from app.routes import cat_breeds


def test_create_breed(test_app, monkeypatch):

    test_request_payload = {
        "breed": "Abyssinian Cat",
        "location_origin": "Ethiopia",
        "coat_length": 0.2,
        "body_type": "Medium long",
        "pattern": "Solid",
    }
    test_response_payload = {"public_id": "something"}

    async def mock_post(payload):
        return {"public_id": "something"}

    monkeypatch.setattr(cat_breeds, "post_cat_breed", mock_post)

    response = test_app.post("/api/cat-breed", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload
