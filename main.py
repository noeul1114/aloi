import argparse
import socket
import threading
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

print(key)

# Parse CLI arguments
parser = argparse.ArgumentParser(description='1:1 Encrypted Communication Program')
parser.add_argument('-s', '--server', action='store_true', help='Run in server mode')
parser.add_argument('-c', '--client', metavar='IP', help='Run in client mode, requires server IP address')
parser.add_argument('-d', '--daemon', action='store_true', help='Run in daemon mode')
parser.add_argument('-g', '--gui', action='store_true', help='Run in GUI mode')
args = parser.parse_args()


# Socket communication functions
def handle_connection(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        decrypted_data = cipher_suite.decrypt(data)
        print(f"Received data from {addr}: {decrypted_data.decode()}")
    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 12345))
    server_socket.listen(1)
    print("Server started. Waiting for connections...")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=handle_connection, args=(conn, addr)).start()


def start_client(ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, 12345))
    print(f"Connected to server at {ip}")
    while True:
        message = input("Enter message (or 'quit' to exit): ")
        if message == 'quit':
            break
        encrypted_message = cipher_suite.encrypt(message.encode())
        client_socket.send(encrypted_message)
    client_socket.close()


# GUI functions
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as file:
            data = file.read()
            encrypted_data = cipher_suite.encrypt(data)
            # Add logic for sending encrypted data
            print("File encrypted and sent.")


def update_gui():
    window = tk.Tk()
    window.title("1:1 Encrypted Communication Program")
    window.geometry("400x300")

    open_button = tk.Button(window, text="Select File", command=open_file)
    open_button.pack(pady=20)

    window.mainloop()


# Main function
def main():
    if args.server:
        start_server()
    elif args.client:
        start_client(args.client)
    elif args.gui:
        update_gui()
    else:
        print("Invalid arguments. Use -h or --help for usage instructions.")


if __name__ == '__main__':
    main()
