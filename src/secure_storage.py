"""
Secure storage utilities using Fernet encryption.

This module provides encryption/decryption for sensitive data storage.
Uses symmetric encryption with key management.

Features:
- Key generation and loading.
- Data encryption/decryption.
- File hashing and verification.
- Backup and restore functionality.
- Secure wipe for file deletion.

Security Notes:
- Keys stored in plaintext (secure key management recommended).
- Uses Fernet (AES 128) for encryption.
- Hashes use SHA256.

Dependencies:
- cryptography (Fernet).
- hashlib for hashing.
- os for file operations.
"""
from cryptography.fernet import Fernet
import hashlib
import os
import json
import random

SECURE_FILE = "secure_data.enc"
KEY_FILE = "secret.key"
HASH_FILE = "file_hashes.enc"
BACKUP_FILE = "file_backup.enc"


def generate_key():
    """
    Generate a new Fernet key and save to file.

    Overwrites existing key if present.
    """
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Load Fernet key from file.

    Returns:
        Key bytes for encryption/decryption.
    """
    return open(KEY_FILE, "rb").read()


def encrypt_data(data, file_path):
    """
    Encrypt string data and save to file.

    Args:
        data: String to encrypt.
        file_path: Path to save encrypted data.
    """
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    with open(file_path, "wb") as file:
        file.write(encrypted_data)


def encrypt_binary(data_bytes: bytes, file_path: str):
    """
    Encrypt raw bytes and save to file.

    Args:
        data_bytes: Bytes to encrypt.
        file_path: Path to save encrypted data.
    """
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted = cipher_suite.encrypt(data_bytes)
    with open(file_path, "wb") as f:
        f.write(encrypted)


def decrypt_binary(file_path: str) -> bytes:
    """
    Decrypt bytes from file.

    Args:
        file_path: Path to encrypted file.

    Returns:
        Decrypted bytes.
    """
    key = load_key()
    cipher_suite = Fernet(key)
    with open(file_path, "rb") as f:
        encrypted = f.read()
    return cipher_suite.decrypt(encrypted)


def encrypt_image(src_path: str, dest_path: str):
    """
    Encrypt an image file.

    Args:
        src_path: Source image file path.
        dest_path: Destination encrypted file path.
    """
    with open(src_path, "rb") as f:
        data = f.read()
    encrypt_binary(data, dest_path)


def decrypt_image(enc_path: str, out_path: str):
    """
    Decrypt an image file.

    Args:
        enc_path: Encrypted file path.
        out_path: Output decrypted image path.
    """
    data = decrypt_binary(enc_path)
    with open(out_path, "wb") as f:
        f.write(data)


def decrypt_data(file_path):
    """
    Decrypt string data from file.

    Args:
        file_path: Path to encrypted file.

    Returns:
        Decrypted string.
    """
    key = load_key()
    cipher_suite = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data


def generate_file_hash(file_path):
    """
    Generate SHA256 hash of file contents.

    Args:
        file_path: Path to file to hash.

    Returns:
        Hex string hash.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()


def save_file_hashes(file_paths):
    """
    Save hashes of multiple files.

    Args:
        file_paths: List of file paths to hash and save.
    """
    file_hashes = {file_path: generate_file_hash(file_path) for file_path in file_paths}
    encrypt_data(json.dumps(file_hashes), HASH_FILE)


def verify_file_hashes(file_paths):
    """
    Verify files against stored hashes.

    Args:
        file_paths: List of file paths to verify.

    Returns:
        (success: bool, failed_file: str or error).
    """
    try:
        decrypted_data = decrypt_data(HASH_FILE)
        stored_hashes = json.loads(decrypted_data)
        for file_path in file_paths:
            current_hash = generate_file_hash(file_path)
            if stored_hashes.get(file_path) != current_hash:
                return False, file_path
        return True, None
    except Exception as e:
        return False, str(e)


def create_backup(file_paths):
    """
    Create encrypted backup of files.

    Args:
        file_paths: List of file paths to backup.
    """
    backup_data = {}
    for file_path in file_paths:
        with open(file_path, "r") as file:
            backup_data[file_path] = file.read()
    encrypt_data(json.dumps(backup_data), BACKUP_FILE)


def restore_files_from_backup():
    """
    Restore files from encrypted backup.
    """
    decrypted_data = decrypt_data(BACKUP_FILE)
    backup_data = json.loads(decrypted_data)
    for file_path, content in backup_data.items():
        with open(file_path, "w") as file:
            file.write(content)
        message = f"File {file_path} restored from backup."
        print(message)
        # speak(message)  # Assuming speak function exists elsewhere


def secure_wipe(file_path):
    """
    Securely wipe file by overwriting with random data.

    Args:
        file_path: Path to file to wipe.
    """
    if os.path.exists(file_path):
        with open(file_path, "r+b") as file:
            length = os.path.getsize(file_path)
            file.write(bytearray(random.getrandbits(8) for _ in range(length)))
        os.remove(file_path)


if __name__ == "__main__":
    if not os.path.exists(KEY_FILE):
        generate_key()