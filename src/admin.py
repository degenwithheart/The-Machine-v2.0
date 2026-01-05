"""Admin utilities and management with ECC security"""
import os
from src.secure_storage import ECCSecureStorage

class AdminManager:
    def __init__(self):
        self.storage = ECCSecureStorage()
        self.admin_password = "default"
        try:
            self.data = self.storage.load_data(password=self.admin_password)
        except:
            self.data = {}
    
    def verify_password(self, password):
        """Verify admin password with double SHA256"""
        admin = self.data.get('admin', {})
        stored_hash = admin.get('password', '')
        return self.storage.verify_password(password, stored_hash)
    
    def change_password(self, old_pass, new_pass):
        """Change admin password and re-encrypt data"""
        if self.verify_password(old_pass):
            self.data['admin']['password'] = self.storage.double_hash_password(new_pass)
            self.storage.save_data(self.data, new_pass)
            self.admin_password = new_pass
            return True
        return False
    
    def list_known_faces(self):
        """List all known faces"""
        known_dir = "src/facebase/known_faces"
        if os.path.exists(known_dir):
            return [f for f in os.listdir(known_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        return []
    
    def list_unknown_faces(self):
        """List all unknown faces"""
        unknown_dir = "src/facebase/unknown_faces"
        if os.path.exists(unknown_dir):
            return [f for f in os.listdir(unknown_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        return []
    
    def get_stats(self):
        """Get system statistics"""
        return {
            'known_faces': len(self.list_known_faces()),
            'unknown_faces': len(self.list_unknown_faces()),
            'admin_enrolled': self.data.get('admin', {}).get('face_enrolled', False),
            'public_key': self.storage.get_public_key_address(),
            'ecc_curve': 'SECP256k1 (Bitcoin)'
        }
    
    def add_face_to_known(self, unknown_filename, person_name):
        """Move unknown face to known faces with name"""
        unknown_path = os.path.join("src/facebase/unknown_faces", unknown_filename)
        known_path = os.path.join("src/facebase/known_faces", f"{person_name}.jpg")
        
        if os.path.exists(unknown_path):
            try:
                import shutil
                shutil.copy2(unknown_path, known_path)
                print(f"Added {person_name} to known faces")
                return True
            except Exception as e:
                print(f"Error adding face: {e}")
                return False
        return False
