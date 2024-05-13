import socket
from encryption import encrypt_message, load_key

def send_message(host, port, message, keyfile):
    key = load_key(keyfile)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        encrypted_message = encrypt_message(message, key)
        print(f"Sending encrypted message: {encrypted_message}")
        client_socket.sendall(encrypted_message)
