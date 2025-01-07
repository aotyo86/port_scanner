from flask import Flask, request, jsonify
from flask import Flask, render_template, send_from_directory
import socket

def scan_ports(ip,start_port,end_port):
    open_ports = []
    for port in range(start_port,end_port+1):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip,port)) == 0:
                open_ports.append(port)
    return open_ports

# テスト

if __name__ == "__main__":
    ip = "127.0.0.1"
    start_port = 1
    end_port = 100
    print(f"Open ports on {ip} : {scan_ports(ip, start_port, end_port)}")

app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# index.htmlを表示するルート
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST','GET'])
def scan():
    data = request.json
    ip = data['ip']
    start_port = data['start_port']
    end_port = data['end_port']
    open_ports = scan_ports(ip,start_port,end_port)
    return jsonify({"open_ports": open_ports})

if __name__ == "__main__":
    app.run(debug=True)