from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/product', methods=['POST'])
def receive_product():
    data = request.json
    print("📦 Nhận dữ liệu:", data)
    return jsonify({"status": "success", "message": "Đã nhận thành công!"}), 200

@app.route('/', methods=['GET'])
def home():
    return "Server đang chạy ngon lành!", 200

if __name__ == '__main__':
    app.run()
