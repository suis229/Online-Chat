import socket
import threading
import sys
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 4096

def recieve_message():
    while True:
        data, _ = client_socket.recvfrom(BUFFER_SIZE)

        if data.decode('utf-8') == "timeout":
            print("タイムアウトしました")
            os._exit(0)
            break
        
        usernamelen = data[0]
        username = data[1:usernamelen+1].decode('utf-8')
        message = data[usernamelen+1:].decode('utf-8')
        print(f"[{username}] {message}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("ユーザ名を入力してください：")
usernamelen = len(username)

if usernamelen > 255:
    print("ユーザ名が長すぎます。短いユーザ名にしてください。")
    sys.exit()

threading.Thread(target=recieve_message, daemon=True).start()

while True:
    message = input()

    data = usernamelen.to_bytes(1, 'big') + username.encode('utf-8') + message.encode('utf-8')
    client_socket.sendto(data, (SERVER_IP, SERVER_PORT))
