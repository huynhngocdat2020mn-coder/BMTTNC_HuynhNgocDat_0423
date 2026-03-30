import socket
import ssl
import threading

# 1. Thông tin server
server_address = ('localhost', 12345)

# 2. Hàm nhận dữ liệu từ server
def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print(f"\nNhận: {data.decode('utf-8')}")
    except:
        pass
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

# 3. Tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 4. Tạo SSL context cho Client
# PROTOCOL_TLS_CLIENT sẽ tự động thiết lập các tùy chọn bảo mật phù hợp
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Vì chúng ta dùng chứng chỉ tự ký (Self-signed), cần tắt kiểm tra hostname và verify
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# 5. Thiết lập kết nối SSL
try:
    ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    ssl_socket.connect(server_address)

    # Bắt đầu một luồng để nhận dữ liệu từ server liên tục
    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
    receive_thread.start()

    # 6. Gửi dữ liệu lên server
    print("--- Đã kết nối bảo mật thành công ---")
    while True:
        message = input("Nhập tin nhắn: ")
        if message.lower() == 'exit':
            break
        ssl_socket.send(message.encode('utf-8'))

except Exception as e:
    print(f"Lỗi kết nối: {e}")
finally:
    if 'ssl_socket' in locals():
        ssl_socket.close()