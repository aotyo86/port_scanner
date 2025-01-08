from flask import Flask, request, jsonify
from flask import render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import socket

app = Flask(__name__)

# SQLiteのデータベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scan_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# データベースモデルの作成
# データベースモデルの作成
class PortScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), nullable=False, unique=True)  # IPアドレスをユニークに設定
    port = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String(50), nullable=True)

# 過去にスキャンしたIPアドレスを取得するエンドポイント
@app.route('/scan_history', methods=['GET'])
def scan_history():
    # スキャン履歴から重複を排除したIPアドレスを取得
    ip_addresses = PortScanResult.query.distinct(PortScanResult.ip).all()
    ip_list = [ip.ip for ip in ip_addresses]
    history = ["127.0.0.1", "192.168.1.1", "10.0.0.1"]
    return jsonify({"history":history})

# ポート番号に対応するサービス名の辞書
PORT_TO_SERVICE = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    3306: "MySQL",
    8080: "HTTP-alt",
    # 他のポート番号とサービス名を追加可能
}

def save_search(ip):
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO search_history (ip) VALUES (?)",(ip,))
    conn.commit()
    conn.close()


def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                # ポート番号に対応するサービス名を取得
                service = PORT_TO_SERVICE.get(port, "Unknown")
                open_ports.append({"port": port, "service": service})
    return open_ports

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
    start_port = int(data.get('start_port'))
    end_port = int(data.get('end_port'))

    # データベースに検索を保存
    save_search(ip)

    # デバッグ用に受け取った値を出力
    print(f"IP: {ip}, Start Port: {start_port}, End Port: {end_port}")

    # 入力値が正しいかチェック
    if not ip or not isinstance(start_port, int) or not isinstance(end_port, int):
        return jsonify({"error": "Invalid input values"}), 400

    open_ports = scan_ports(ip, start_port, end_port)
    return jsonify({"open_ports": open_ports})

@app.route('/history',methods=['GET'])
def get_history():
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute("SELELCT ip FROM search_history ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    #過去のIPリストをJSON形式で返す
    ip_list = [row[0] for row in rows]
    return jsonify({"history": ip_list})

if __name__ == "__main__":
    app.run(debug=True)
