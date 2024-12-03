from flask import Flask, request, jsonify
import uuid
from utils import calculate_points
import redis
import json
import os

redis_host = os.getenv("REDIS_HOST", "localhost")

app = Flask(__name__)
redis_client = redis.Redis(host="redis", port=6379, db=0)


@app.route("/")
def main():
    return jsonify(
        {
            "guide": "use /receipts/process to process receipts and receipts/<receipt_id>/points to get points of specific id "
        }
    )


@app.route("/receipts/process", methods=["POST"])
def process_receipts():
    receipt = request.json

    if not receipt:
        return jsonify({"error": "Invalid receipt data"}), 400

    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    redis_client.set(receipt_id, json.dumps({"points": points}))

    return jsonify({"id": receipt_id})


@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    response = redis_client.get(receipt_id)

    if not response:
        return jsonify({"error": "Receipt not found"}), 404

    response = json.loads(response)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
