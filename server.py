import socket
from encryption import decrypt_message, load_key


def start_server(host, port, keyfile):
    key = load_key(keyfile)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening on {host}:{port}...")

        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Connected by {client_address}")
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                print(f"Received encrypted message: {message}")
                print("Decrypting message...")
                decrypted_message = decrypt_message(message, key)
                print(f"Decrypted message: {decrypted_message}")

