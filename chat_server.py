import socket
import threading
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 4096
TIMEOUT = 30  # タイムアウトまでの時間

# クライアント情報を保持 {クライアントアドレス：最終メッセージ送信時間}
clients = {}

def remove_inactive_clients():
    while True:
        current_time = time.time()
        copy_clients = clients.copy()
        for client in copy_clients.keys():
            if current_time - copy_clients[client] > TIMEOUT:
                print(f"クライアント {client} がタイムアウトしました")
                message = "timeout".encode('utf-8')
                server_socket.sendto(message, client)
                del clients[client]
        time.sleep(1)

# クライアントからのメッセージを他のクライアントへ送信
def handle_client_message(data, client_address):
    usernamelen = data[0]
    username = data[1:usernamelen+1].decode('utf-8')
    message = data[usernamelen+1:].decode('utf-8')
    print(f"[{username}] {message}")

    clients[client_address] = time.time()

    for client in clients.keys():
        if client != client_address:
            try:
                server_socket.sendto(data, client)
            except Exception as e:
                print(f"クライアントへメッセージを送信できませんでした: {e}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"サーバ {SERVER_IP}:{SERVER_PORT} が起動しました...")

threading.Thread(target=remove_inactive_clients, daemon=True).start()

while True:
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    handle_client_message(data, client_address)
