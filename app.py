from flask import Flask, request, jsonify
from flask import render_template, send_from_directory
import socket

def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    return open_ports

# テスト
if __name__ == "__main__":
    ip = "127.0.0.1"
    start_port = 1
    end_port = 100
    print(f"Open ports on {ip}: {scan_ports(ip, start_port, end_port)}")

app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# index.htmlを表示するルート
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST', 'GET'])
def scan():
    data = request.get_json()  # JSONデータを取得
    # デバッグ用の出力を追加
    print("Received Data:", data)
    if not data:
        return jsonify({"error": "No data received or invalid JSON format"}), 400

    ip = data.get('ip')
    start_port = data.get('start_port')
    end_port = data.get('end_port')

    # デバッグ用に受け取った値を出力
    print(f"IP: {ip}, Start Port: {start_port}, End Port: {end_port}")

    # 入力値が正しいかチェック
    if not ip or not isinstance(start_port, int) or not isinstance(end_port, int):
        return jsonify({"error": "Invalid input values"}), 400

    open_ports = scan_ports(ip, start_port, end_port)
    open_ports = [{"port": port, "service": "Unknown"} for port in open_ports]
    return jsonify({"open_ports": open_ports})

if __name__ == "__main__":
    app.run(debug=True)
