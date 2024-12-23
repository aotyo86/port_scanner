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