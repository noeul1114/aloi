import argparse
import sys
import threading
from server import start_server
from client import send_message
from encryption import generate_key, save_key

def main():
    parser = argparse.ArgumentParser(description="1:1 Encrypted Communication Program")
    parser.add_argument("-m", "--mode", choices=["server", "client", "keygen"], help="Mode of operation")
    parser.add_argument("-H", "--host", type=str, help="Host address (for client or server)")
    parser.add_argument("-p", "--port", type=int, help="Port number (for client or server)")
    parser.add_argument("-k", "--keyfile", type=str, help="File containing symmetric key")
    parser.add_argument("-t", "--text", type=str, help="Text to send (client mode only)")
    args = parser.parse_args()

    if args.mode == "keygen":
        if not args.keyfile:
            print("Please specify a keyfile with -k or --keyfile.")
            sys.exit(1)
        key = generate_key()
        save_key(key, args.keyfile)
        print(f"Generated key and saved to {args.keyfile}")
    elif args.mode == "server":
        if not args.host or not args.port or not args.keyfile:
            print("Server mode requires -H (host), -p (port), and -k (keyfile).")
            sys.exit(1)
        server_thread = threading.Thread(target=start_server, args=(args.host, args.port, args.keyfile))
        server_thread.start()
    elif args.mode == "client":
        if not args.host or not args.port or not args.keyfile or not args.text:
            print("Client mode requires -H (host), -p (port), -k (keyfile), and -t (text).")
            sys.exit(1)
        send_message(args.host, args.port, args.text, args.keyfile)

if __name__ == "__main__":
    main()
