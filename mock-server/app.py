import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

def load_customers():
    path = os.path.join(os.path.dirname(__file__), "data", "customers.json")
    with open(path) as f:
        return json.load(f)

customers = load_customers()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/customers", methods=["GET"])
def list_customers():
    page = max(1, request.args.get("page", 1, type=int))
    limit = min(100, max(1, request.args.get("limit", 10, type=int)))
    total = len(customers)
    start = (page - 1) * limit
    end = start + limit
    data = customers[start:end]
    return jsonify({
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    for c in customers:
        if c["customer_id"] == customer_id:
            return jsonify(c)
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
