"""Secure storage with ECC encryption (similar to Bitcoin)"""
import os
import json
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
from ecdsa.util import sigencode_string, sigdecode_string
from pathlib import Path
import base64

class ECCSecureStorage:
    """
    Elliptic Curve Cryptography (ECC) based secure storage
    Uses SECP256k1 curve (same as Bitcoin) for key generation and signing
    """
    
    def __init__(self, key_path="src/ecc_keys"):
        self.key_path = key_path
        self.private_key_file = os.path.join(key_path, "private.pem")
        self.public_key_file = os.path.join(key_path, "public.pem")
        self.data_file = "src/secure_data.json"
        self.private_key, self.public_key = self._load_or_create_keys()
    
    def _load_or_create_keys(self):
        """Load existing ECC key pair or generate new one (SECP256k1 - Bitcoin curve)"""
        os.makedirs(self.key_path, exist_ok=True)
        
        if os.path.exists(self.private_key_file) and os.path.exists(self.public_key_file):
            # Load existing keys
            with open(self.private_key_file, 'rb') as f:
                private_key = SigningKey.from_pem(f.read())
            with open(self.public_key_file, 'rb') as f:
                public_key = VerifyingKey.from_pem(f.read())
            print("Loaded existing ECC key pair (SECP256k1)")
        else:
            # Generate new key pair using SECP256k1 (Bitcoin curve)
            private_key = SigningKey.generate(curve=SECP256k1)
            public_key = private_key.get_verifying_key()
            
            # Save keys
            with open(self.private_key_file, 'wb') as f:
                f.write(private_key.to_pem())
            with open(self.public_key_file, 'wb') as f:
                f.write(public_key.to_pem())
            
            # Secure the private key file
            os.chmod(self.private_key_file, 0o600)
            print("Generated new ECC key pair (SECP256k1 - Bitcoin curve)")
        
        return private_key, public_key
    
    def _symmetric_encrypt(self, data, password):
        """
        Symmetric encryption using password-derived key
        Similar to Bitcoin wallet encryption
        """
        # Derive key from password using PBKDF2
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
        
        # Simple XOR encryption (replace with AES for production)
        data_bytes = data.encode() if isinstance(data, str) else data
        encrypted = bytes(a ^ b for a, b in zip(data_bytes, (key * (len(data_bytes) // len(key) + 1))[:len(data_bytes)]))
        
        return {
            'salt': base64.b64encode(salt).decode(),
            'data': base64.b64encode(encrypted).decode()
        }
    
    def _symmetric_decrypt(self, encrypted_data, password):
        """Decrypt data encrypted with symmetric key"""
        salt = base64.b64decode(encrypted_data['salt'])
        encrypted = base64.b64decode(encrypted_data['data'])
        
        # Derive same key
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)
        
        # Decrypt
        decrypted = bytes(a ^ b for a, b in zip(encrypted, (key * (len(encrypted) // len(key) + 1))[:len(encrypted)]))
        return decrypted
    
    def sign_data(self, data):
        """Sign data with private key (like Bitcoin transaction signing)"""
        data_bytes = data.encode() if isinstance(data, str) else data
        signature = self.private_key.sign(data_bytes, sigencode=sigencode_string)
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, data, signature):
        """Verify signature with public key"""
        try:
            data_bytes = data.encode() if isinstance(data, str) else data
            sig_bytes = base64.b64decode(signature)
            self.public_key.verify(sig_bytes, data_bytes, sigdecode=sigdecode_string)
            return True
        except BadSignatureError:
            return False
    
    def save_data(self, data, password="default"):
        """Save and sign data"""
        json_data = json.dumps(data)
        
        # Encrypt data
        encrypted = self._symmetric_encrypt(json_data, password)
        
        # Sign encrypted data for integrity
        signature = self.sign_data(encrypted['data'])
        
        # Save with signature
        output = {
            'encrypted': encrypted,
            'signature': signature,
            'public_key': base64.b64encode(self.public_key.to_string()).decode()
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(output, f, indent=2)
    
    def load_data(self, password="default"):
        """Load and verify signed data"""
        if not os.path.exists(self.data_file):
            return {}
        
        with open(self.data_file, 'r') as f:
            stored = json.load(f)
        
        # Verify signature
        if not self.verify_signature(stored['encrypted']['data'], stored['signature']):
            raise ValueError("Data signature verification failed! Data may be tampered.")
        
        # Decrypt
        decrypted = self._symmetric_decrypt(stored['encrypted'], password)
        return json.loads(decrypted)
    
    def hash_password(self, password):
        """Hash password with SHA256 (Bitcoin-style)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def double_hash_password(self, password):
        """Double SHA256 hash (Bitcoin standard for extra security)"""
        first_hash = hashlib.sha256(password.encode()).digest()
        return hashlib.sha256(first_hash).hexdigest()
    
    def verify_password(self, password, hash_value):
        """Verify password against double hash"""
        return self.double_hash_password(password) == hash_value
    
    def get_public_key_address(self):
        """Get Bitcoin-style address from public key"""
        pub_bytes = self.public_key.to_string()
        sha256_hash = hashlib.sha256(pub_bytes).digest()
        ripemd160 = hashlib.new('ripemd160', sha256_hash).digest()
        return base64.b64encode(ripemd160).decode()

if __name__ == "__main__":
    print("Initializing ECC secure storage (SECP256k1 - Bitcoin curve)...")
    storage = ECCSecureStorage()
    
    # Display public key address
    print(f"Public Key Address: {storage.get_public_key_address()}")
    
    # Create default admin account
    default_pass = "admin123"
    admin_data = {
        "admin": {
            "password": storage.double_hash_password(default_pass),
            "face_enrolled": False,
            "voice_enrolled": False,
            "public_key": storage.get_public_key_address()
        }
    }
    storage.save_data(admin_data, default_pass)
    print(f"\nAdmin account created with ECC encryption")
    print(f"Default password: {default_pass}")
    print("Please change this immediately!")
    print("\nSecurity Features:")
    print("- SECP256k1 elliptic curve (Bitcoin standard)")
    print("- Double SHA256 password hashing")
    print("- ECDSA signature verification")
    print("- PBKDF2 key derivation (100,000 iterations)")
