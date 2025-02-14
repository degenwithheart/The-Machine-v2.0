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
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_data(data, file_path):
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_data(file_path):
    key = load_key()
    cipher_suite = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def generate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def save_file_hashes(file_paths):
    file_hashes = {file_path: generate_file_hash(file_path) for file_path in file_paths}
    encrypt_data(json.dumps(file_hashes), HASH_FILE)

def verify_file_hashes(file_paths):
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
    backup_data = {}
    for file_path in file_paths:
        with open(file_path, "r") as file:
            backup_data[file_path] = file.read()
    encrypt_data(json.dumps(backup_data), BACKUP_FILE)

def restore_files_from_backup():
    decrypted_data = decrypt_data(BACKUP_FILE)
    backup_data = json.loads(decrypted_data)
    for file_path, content in backup_data.items():
        with open(file_path, "w") as file:
            file.write(content)
        message = f"File {file_path} restored from backup."
        print(message)
        speak(message)

def secure_wipe(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r+b") as file:
            length = os.path.getsize(file_path)
            file.write(bytearray(random.getrandbits(8) for _ in range(length)))
        os.remove(file_path)

if __name__ == "__main__":
    if not os.path.exists(KEY_FILE):
        generate_key()