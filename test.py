import json
import uuid
import pytest
from flask import Flask
from fakeredis import FakeRedis
from endpoints import app, calculate_points
import os


TEST_RECEIPTS_DIR = "test_receipts"


# Dynamically load JSON test data from the directory
def load_test_receipts():
    test_cases = []
    for filename in os.listdir(TEST_RECEIPTS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(TEST_RECEIPTS_DIR, filename), "r") as file:
                receipt = json.load(file)
                test_cases.append((filename, receipt))
    return test_cases


# Parameterize the test with all JSON files in the directory
@pytest.mark.parametrize("filename,receipt", load_test_receipts())
def test_calculate_points(filename, receipt):

    expected_points = receipt.pop("expected_points", None)
    assert (
        expected_points is not None
    ), f"{filename} must contain an 'expected_points' field"

    calculated_points = calculate_points(receipt)
    assert (
        calculated_points == expected_points
    ), f"{filename}: Expected {expected_points} points, got {calculated_points}"


# Set up a fake Redis instance for testing
@pytest.fixture
def fake_redis():
    redis_client = FakeRedis()
    yield redis_client
    redis_client.flushall()


# Configure the Flask app for testing
@pytest.fixture
def client(fake_redis, monkeypatch):

    monkeypatch.setattr("endpoints.redis_client", fake_redis)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test the /receipts/process endpoint
def test_process_receipts(client, fake_redis):
    with open("test_receipts/simple-receipt.json", "r") as file:
        test_data = json.load(file)
    response = client.post("/receipts/process", json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data

    receipt_id = data["id"]

    stored_data = fake_redis.get(receipt_id)
    assert stored_data is not None

    points = json.loads(stored_data)["points"]
    assert points == 31


# Test the /receipts/{id}/points endpoint
def test_get_points(client, fake_redis):

    receipt_id = str(uuid.uuid4())
    fake_redis.set(receipt_id, json.dumps({"points": 92}))

    response = client.get(f"/receipts/{receipt_id}/points")
    assert response.status_code == 200

    data = response.get_json()
    assert "points" in data
    assert data["points"] == 92


# Test /receipts/{id}/points for a missing receipt
def test_get_points_missing_receipt(client):
    invalid_id = str(uuid.uuid4())
    response = client.get(f"/receipts/{invalid_id}/points")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Receipt not found"


# Test /receipts/process for invalid data
def test_process_receipts_invalid_data(client):
    response = client.post("/receipts/process", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid receipt data"
