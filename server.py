from flask import Flask, request, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("API_KEY")

UPI_ID = "bhojabikazim2004@okhdfcbank"


# ==============================
# Database Connection
# ==============================
def get_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not set")
    return psycopg2.connect(DATABASE_URL)


def init_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id VARCHAR(100) PRIMARY KEY,
                        amount NUMERIC,
                        status VARCHAR(20),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        print("Database initialized.")
    except Exception as e:
        print("DB Init Error:", e)


init_db()


# ==============================
# API Key Middleware
# ==============================
def require_api_key(req):
    return req.headers.get("X-API-KEY") == API_KEY


# ==============================
# Generate QR Endpoint
# ==============================
@app.route("/generate_qr", methods=["POST"])
def generate_qr():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "amount" not in data or "order_id" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    amount = data["amount"]
    order_id = data["order_id"]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO orders (order_id, amount, status)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (order_id) DO NOTHING
                """, (order_id, amount, "pending"))
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

    upi_link = f"upi://pay?pa={UPI_ID}&pn=Kazim%20Bhojani&am={amount}&tn={order_id}&cu=INR"

    return jsonify({"upi_link": upi_link}), 200


# ==============================
# Check Payment Status
# ==============================
@app.route("/check_status", methods=["GET"])
def check_status():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify({"error": "order_id is required"}), 400

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
                order = cur.fetchone()

        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({"status": order["status"]}), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


# ==============================
# Admin: Get All Orders
# ==============================
@app.route("/admin/orders", methods=["GET"])
def get_all_orders():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
                orders = cur.fetchall()

        return jsonify(orders), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


# ==============================
# Admin: Update Order Status
# ==============================
@app.route("/admin/update_status", methods=["POST"])
def update_status():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "order_id" not in data or "status" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    order_id = data["order_id"]
    status = data["status"]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE orders
                    SET status = %s
                    WHERE order_id = %s
                """, (status, order_id))

        return jsonify({"message": "Status updated"}), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


# ==============================
# Run Server
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)