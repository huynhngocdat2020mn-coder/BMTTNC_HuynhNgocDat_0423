import socket
import ssl
import threading

# 1. Cấu hình địa chỉ Server
server_address = ('localhost', 12345)
clients = []

# 2. Hàm xử lý từng Client (Đa luồng)
def handle_client(client_socket):
    clients.append(client_socket)
    print(f"Đã kết nối với: {client_socket.getpeername()}")
    
    try:
        while True:
            # Nhận dữ liệu từ client (tối đa 1024 bytes)
            data = client_socket.recv(1024)
            if not data:
                break
            
            print(f"Nhận: {data.decode('utf-8')}")
            
            # Gửi dữ liệu nhận được đến tất cả các client khác
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                    except:
                        clients.remove(client)
    except:
        pass
    finally:
        # Ngắt kết nối và dọn dẹp danh sách
        print(f"Đã ngắt kết nối: {client_socket.getpeername()}")
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# 3. Khởi tạo Socket Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server đang chờ kết nối qua SSL...")

# 4. Lắng nghe và thiết lập SSL cho mỗi kết nối
while True:
    client_socket, client_address = server_socket.accept()
    
    # Tạo SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Nạp chứng chỉ (Đảm bảo file .crt và .key nằm trong thư mục certificates)
    try:
        context.load_cert_chain(
            certfile="./certificates/server-cert.crt", 
            keyfile="./certificates/server-key.key"
        )
        
        # Bọc (wrap) socket thông thường bằng lớp bảo mật SSL
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        
        # Tạo luồng xử lý riêng cho mỗi client
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
        client_thread.start()
    except Exception as e:
        print(f"Lỗi thiết lập SSL: {e}")
        client_socket.close()