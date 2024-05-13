from cryptography.fernet import Fernet

def generate_key():
    """Generate a symmetric encryption key."""
    return Fernet.generate_key()

def save_key(key, filename):
    """Save the key to a file."""
    with open(filename, "wb") as key_file:
        key_file.write(key)

def load_key(filename):
    """Load the key from a file."""
    with open(filename, "rb") as key_file:
        return key_file.read()

def encrypt_message(message, key):
    """Encrypt the message."""
    return Fernet(key).encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    """Decrypt the message."""
    return Fernet(key).decrypt(encrypted_message).decode()
