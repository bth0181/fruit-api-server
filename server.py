from flask import Flask, request, jsonify, render_template_string
import uuid
import qrcode
import io
import base64

app = Flask(__name__)
orders = []  # Danh sách lưu đơn hàng

# Nhận dữ liệu từ Raspberry Pi
@app.route('/product', methods=['POST'])
def receive_product():
    data = request.get_json()
    data["id"] = str(uuid.uuid4())  # Gán ID duy nhất cho mỗi đơn
    orders.append(data)
    print("📦 Nhận dữ liệu:", data)
    return jsonify({"status": "success", "message": "Đã nhận thành công!"}), 200

# Hiển thị đơn hàng với nút XÓA & CHECKOUT
@app.route('/orders', methods=['GET'])
def show_orders_fancy():
    html = """
    <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Đơn hàng</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; padding: 30px; }
        .card { background: white; border-radius: 15px; box-shadow: 0 2px 10px #ccc;
                margin-bottom: 20px; padding: 20px; display: flex; align-items: center; justify-content: space-between; }
        .info { flex: 1; margin-left: 20px; }
        .info div { margin: 4px 0; }
        .pay { font-weight: bold; background: #00bcd4; color: white; padding: 10px 20px; border-radius: 10px; }
        .buttons { display: flex; gap: 10px; margin-bottom: 40px; }
        .buttons a { text-decoration: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; }
        .checkout { background: #00bcd4; color: white; }
        .delete { background: red; color: white; }
    </style>
    </head><body>
    <h2>🧾 ĐƠN HÀNG TRÁI CÂY</h2>
    {% for order in orders %}
        {% for item in order.products %}
            <div class="card">
                <img src="https://via.placeholder.com/60?text={{item.name[0]|upper}}" />
                <div class="info">
                    <div><strong>PRODUCT NAME:</strong> {{ item.name.upper() }}</div>
                    <div><strong>PER UNIT:</strong> {{ item.unit_price }}k</div>
                    <div><strong>UNITS:</strong> {{ item.quantity }} trái</div>
                </div>
                <div class="pay">{{ item.total_price }}k</div>
            </div>
        {% endfor %}
        <div class="buttons">
            <a class="checkout" href="/checkout/{{ order.id }}">CHECKOUT {{ order.total_amount }}k</a>
            <a class="delete" href="/delete/{{ order.id }}">XÓA</a>
        </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, orders=orders)

# XÓA đơn hàng
@app.route('/delete/<id>')
def delete_order(id):
    global orders
    orders = [o for o in orders if o["id"] != id]
    return "<script>location.href='/orders'</script>"

# HIỂN THỊ QR GIẢ – hiện dòng chữ tổng tiền khi quét
@app.route('/checkout/<id>')
def checkout_qr(id):
    order = next((o for o in orders if o["id"] == id), None)
    if not order:
        return "❌ Không tìm thấy đơn hàng"

    total = order["total_amount"]
    data = f"THANH TOÁN {total}k"

    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")

    html = f"""
    <html><body style="text-align:center; font-family:sans-serif; padding-top:50px;">
        <h2>💳 Quét QR để thanh toán</h2>
        <p><strong>Số tiền:</strong> {total}k</p>
        <img src="data:image/png;base64,{encoded}" width="220"/>
        <br><br>
        <a href='/orders'>⬅️ Quay lại</a>
    </body></html>
    """
    return html

# Trang mặc định
@app.route('/')
def index():
    return "<h3>✅ Server đang chạy – <a href='/orders'>Xem đơn hàng</a></h3>"

if __name__ == '__main__':
    app.run()
