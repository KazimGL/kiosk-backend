from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

# In-memory database (for testing)
orders_db = {}

# UPI details
UPI_ID = "bhojabikazim2004@okhdfcbank"
NAME = "Kazim Bhojani"


# ==============================
# Endpoint 1: Generate QR Code
# ==============================
@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.get_json()

    if not data or "amount" not in data or "order_id" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    amount = data["amount"]
    order_id = data["order_id"]

    # Save order
    orders_db[order_id] = {
        "amount": amount,
        "status": "pending",
        "created_at": time.time()
    }

    # Generate UPI URI
    upi_link = f"upi://pay?pa={UPI_ID}&pn=Kazim%20Bhojani&am={amount}&tn={order_id}&cu=INR"

    return jsonify({
        "upi_link": upi_link
    }), 200


# ==============================
# Endpoint 2: Check Payment Status
# ==============================
@app.route("/check_status", methods=["GET"])
def check_status():

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify({"error": "order_id is required"}), 400

    if order_id not in orders_db:
        return jsonify({"error": "Order not found"}), 404

    order = orders_db[order_id]

    # Simulate success after 15 seconds
    if order["status"] == "pending":
        if time.time() - order["created_at"] > 15:
            order["status"] = "success"

    return jsonify({
        "status": order["status"]
    }), 200


# ==============================
# Run Server (Render Compatible)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)