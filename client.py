import socket
import threading
from encryption import encrypt_message, decrypt_message, load_key


def receive_messages(client_socket, key):
    """Receive messages from the server."""
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received encrypted message: {message}")
            decrypted_message = decrypt_message(message, key)
            print(f"Decrypted message: {decrypted_message}")
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()


def send_messages(client_socket, key):
    """Send messages to the server."""
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


def send_message(host, port, keyfile):
    key = load_key(keyfile)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Create a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, key))
        receive_thread.start()

        # Main thread will be used to send messages to the server
        send_messages(client_socket, key)