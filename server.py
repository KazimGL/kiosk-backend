# from flask import Flask, request, jsonify
# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = Flask(__name__)

# # ==============================
# # Environment Variables
# # ==============================
# DATABASE_URL = os.environ.get("DATABASE_URL")
# API_KEY = os.environ.get("API_KEY")

# UPI_ID = "bhojabikazim2004@okhdfcbank"

# # ==============================
# # Database Connection
# # ==============================
# def get_connection():
#     return psycopg2.connect(DATABASE_URL)

# # Create table if not exists
# def init_db():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS orders (
#             order_id VARCHAR(100) PRIMARY KEY,
#             amount NUMERIC,
#             status VARCHAR(20),
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# init_db()

# # ==============================
# # API Key Middleware
# # ==============================
# def require_api_key(req):
#     client_key = req.headers.get("X-API-KEY")
#     if client_key != API_KEY:
#         return False
#     return True


# # ==============================
# # Generate QR Endpoint
# # ==============================
# @app.route("/generate_qr", methods=["POST"])
# def generate_qr():

#     if not require_api_key(request):
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.get_json()

#     if not data or "amount" not in data or "order_id" not in data:
#         return jsonify({"error": "Invalid payload"}), 400

#     amount = data["amount"]
#     order_id = data["order_id"]

#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO orders (order_id, amount, status)
#         VALUES (%s, %s, %s)
#         ON CONFLICT (order_id) DO NOTHING
#     """, (order_id, amount, "pending"))

#     conn.commit()
#     cur.close()
#     conn.close()

#     upi_link = f"upi://pay?pa={UPI_ID}&pn=Kazim%20Bhojani&am={amount}&tn={order_id}&cu=INR"

#     return jsonify({"upi_link": upi_link}), 200


# # ==============================
# # Check Payment Status
# # ==============================
# @app.route("/check_status", methods=["GET"])
# def check_status():

#     if not require_api_key(request):
#         return jsonify({"error": "Unauthorized"}), 401

#     order_id = request.args.get("order_id")

#     if not order_id:
#         return jsonify({"error": "order_id is required"}), 400

#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
#     order = cur.fetchone()

#     if not order:
#         cur.close()
#         conn.close()
#         return jsonify({"error": "Order not found"}), 404

#     cur.close()
#     conn.close()

#     return jsonify({"status": order["status"]}), 200


# # ==============================
# # Admin: Get All Orders
# # ==============================
# @app.route("/admin/orders", methods=["GET"])
# def get_all_orders():

#     if not require_api_key(request):
#         return jsonify({"error": "Unauthorized"}), 401

#     conn = get_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
#     orders = cur.fetchall()

#     cur.close()
#     conn.close()

#     return jsonify(orders), 200


# # ==============================
# # Admin: Update Order Status
# # ==============================
# @app.route("/admin/update_status", methods=["POST"])
# def update_status():

#     if not require_api_key(request):
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.get_json()

#     if not data or "order_id" not in data or "status" not in data:
#         return jsonify({"error": "Invalid payload"}), 400

#     order_id = data["order_id"]
#     status = data["status"]

#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         UPDATE orders
#         SET status = %s
#         WHERE order_id = %s
#     """, (status, order_id))

#     conn.commit()
#     cur.close()
#     conn.close()

#     return jsonify({"message": "Status updated"}), 200


# # ==============================
# # Run Server (Render Compatible)
# # ==============================
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
# ====================================================================================================
#                                  NEW   BACKEND 
# ====================================================================================================
from flask import Flask, request, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ==============================
# Environment Variables
# ==============================
DATABASE_URL = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("API_KEY")

UPI_ID = "bhojabikazim2004@okhdfcbank"

# ==============================
# Database Connection
# ==============================
def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Create table if not exists
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id VARCHAR(100) PRIMARY KEY,
            amount NUMERIC,
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# ==============================
# API Key Middleware
# ==============================
def require_api_key(req):
    client_key = req.headers.get("X-API-KEY")
    if client_key != API_KEY:
        return False
    return True


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

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (order_id, amount, status)
        VALUES (%s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
    """, (order_id, amount, "pending"))

    conn.commit()
    cur.close()
    conn.close()

    upi_link = f"upi://pay?pa={UPI_ID}&pn=Kazim%20Bhojani&am={amount}&tn={order_id}&cu=INR"

    return jsonify({"upi_link": upi_link}), 200


# ==============================
# Check Payment Status (WITH 20-SEC AUTO SUCCESS)
# ==============================
@app.route("/check_status", methods=["GET"])
def check_status():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify({"error": "order_id is required"}), 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Ask the database for the order AND how many seconds have passed since creation
    cur.execute("""
        SELECT *, EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - created_at)) AS elapsed 
        FROM orders 
        WHERE order_id = %s
    """, (order_id,))
    order = cur.fetchone()

    if not order:
        cur.close()
        conn.close()
        return jsonify({"error": "Order not found"}), 404

    # --- AUTO SUCCESS LOGIC ---
    # If the order is pending and 20+ seconds have passed, update it to success
    if order["status"] == "pending" and order["elapsed"] >= 20:
        cur.execute("UPDATE orders SET status = 'success' WHERE order_id = %s", (order_id,))
        conn.commit()
        order["status"] = "success"  # Update the response variable to match
        print(f"[API] Order {order_id} automatically marked as SUCCESS after 20 seconds.")
    # --------------------------

    cur.close()
    conn.close()

    return jsonify({"status": order["status"]}), 200


# ==============================
# Admin: Get All Orders
# ==============================
@app.route("/admin/orders", methods=["GET"])
def get_all_orders():

    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(orders), 200


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

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status = %s
        WHERE order_id = %s
    """, (status, order_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Status updated"}), 200


# ==============================
# Run Server (Render Compatible)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)