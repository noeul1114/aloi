import socket
import threading
from encryption import decrypt_message, encrypt_message, load_key


def handle_client(client_socket, key):
    """Handle incoming messages from a client."""
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            # print(f"Received encrypted message: {message}")
            decrypted_message = decrypt_message(message, key)
            print(f"Received decrypted message: {decrypted_message}")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def send_messages(client_socket, key):
    """Send messages to the client."""
    try:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            encrypted_message = encrypt_message(message, key)
            client_socket.sendall(encrypted_message)
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        client_socket.close()


def start_server(host, port, keyfile):
    key = load_key(keyfile)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening on {host}:{port}...")

        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        # Create a thread to handle incoming messages from the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, key))
        client_thread.start()

        # Main thread will be used to send messages to the client
        send_messages(client_socket, key)