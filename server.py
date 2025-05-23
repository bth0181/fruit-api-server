from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
orders = []  # Danh sách lưu các đơn hàng

# Nhận dữ liệu đơn hàng từ Raspberry Pi
@app.route('/product', methods=['POST'])
def receive_product():
    data = request.get_json()
    orders.append(data)
    print("📦 Nhận dữ liệu:", data)
    return jsonify({"status": "success", "message": "Đã nhận thành công!"}), 200

# Giao diện đẹp kiểu ứng dụng để hiển thị đơn hàng
@app.route('/orders', methods=['GET'])
def show_orders_fancy():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Fruit Orders</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f0f2f5;
            padding: 30px;
        }
        .card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card img {
            height: 60px;
            width: 60px;
            border-radius: 50%;
        }
        .info {
            flex: 1;
            margin-left: 20px;
        }
        .info div {
            margin: 4px 0;
        }
        .pay {
            font-weight: bold;
            background: #00bcd4;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
        }
        .checkout {
            text-align: center;
            margin-top: 30px;
        }
        .checkout button {
            background: #00bcd4;
            color: white;
            padding: 15px 30px;
            border: none;
            font-size: 16px;
            border-radius: 30px;
            cursor: pointer;
        }
    </style>
    </head>
    <body>
        <h2>🧾 ĐƠN HÀNG TRÁI CÂY</h2>
        {% for order in orders %}
            {% for item in order.products %}
                <div class="card">
                    <img src="https://via.placeholder.com/60?text={{item.name[0]|upper}}" alt="{{item.name}}">
                    <div class="info">
                        <div><strong>PRODUCT NAME:</strong> {{ item.name.upper() }}</div>
                        <div><strong>PER UNIT:</strong> {{ item.unit_price }}k</div>
                        <div><strong>UNITS:</strong> {{ item.quantity }} trái</div>
                    </div>
                    <div class="pay">{{ item.total_price }}k</div>
                </div>
            {% endfor %}
            <div class="checkout">
                <button>CHECKOUT {{ order.total_amount }}k</button>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, orders=orders)

# Trang mặc định
@app.route('/')
def index():
    return "<h3>✅ Server đang chạy – <a href='/orders'>Xem đơn hàng</a></h3>"

if __name__ == '__main__':
    app.run()
