import socket

def get_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode()
        return banner
    except:
        return None

ip = "127.0.0.1"
port = 22  # SSHの標準ポート
banner = get_banner(ip, port)
if banner and "SSH" in banner:
    print("This port is running SSH.")
else:
    print("This port is not SSH.")
