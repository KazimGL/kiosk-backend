from flask import Flask, request, jsonify
import time

app = Flask(__name__)

orders_db = {}

UPI_ID = "bhojabikazim2004@okhdfcbank"
NAME = "Kazim Bhojani"

@app.route("/generate_qr", methods=["POST"])
def generate_qr():

    data = request.get_json()

    if not data or "amount" not in data or "order_id" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    amount = data["amount"]
    order_id = data["order_id"]

    orders_db[order_id] = {
        "amount": amount,
        "status": "pending",
        "created_at": time.time()
    }

    upi_link = f"upi://pay?pa={UPI_ID}&pn=Kazim%20Bhojani&am={amount}&tn={order_id}&cu=INR"

    return jsonify({"upi_link": upi_link}), 200


@app.route("/check_status", methods=["GET"])
def check_status():

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify({"error": "order_id is required"}), 400

    if order_id not in orders_db:
        return jsonify({"error": "Order not found"}), 404

    order = orders_db[order_id]

    if order["status"] == "pending":
        if time.time() - order["created_at"] > 15:
            order["status"] = "success"

    return jsonify({"status": order["status"]}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)