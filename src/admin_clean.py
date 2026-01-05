"""Clean admin interface with ECC authentication"""
import getpass
import os
from src.admin import AdminManager
from src.ai_adapters import AIAdapter, DeepFaceProvider

class AdminInterface:
    def __init__(self):
        self.manager = AdminManager()
        self.authenticated = False
    
    def authenticate(self):
        """Authenticate admin user with ECC"""
        print("\n" + "="*50)
        print("ADMIN AUTHENTICATION (ECC SECP256k1)")
        print("="*50)
        password = getpass.getpass("Password: ")
        
        if self.manager.verify_password(password):
            self.authenticated = True
            self.manager.admin_password = password
            print("✓ Authentication successful")
            print(f"✓ Public Key: {self.manager.storage.get_public_key_address()}")
            return True
        else:
            print("✗ Authentication failed")
            return False
    
    def show_menu(self):
        """Show admin menu"""
        if not self.authenticated:
            if not self.authenticate():
                return
        
        while True:
            print("\n" + "="*50)
            print("ADMIN PANEL (ECC Secured)")
            print("="*50)
            print("1. View System Statistics")
            print("2. List Known Faces")
            print("3. List Unknown Faces")
            print("4. Add Unknown Face to Database")
            print("5. Change Password")
            print("6. View ECC Public Key")
            print("7. Analyze Face with DeepFace")
            print("8. Test AI Integration")
            print("9. Back to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.show_statistics()
            elif choice == '2':
                self.list_known_faces()
            elif choice == '3':
                self.list_unknown_faces()
            elif choice == '4':
                self.add_unknown_to_known()
            elif choice == '5':
                self.change_password()
            elif choice == '6':
                self.show_public_key()
            elif choice == '7':
                self.analyze_face_deepface()
            elif choice == '8':
                self.test_ai()
            elif choice == '9':
                break
    
    def show_statistics(self):
        """Display system statistics"""
        stats = self.manager.get_stats()
        print("\n" + "="*50)
        print("SYSTEM STATISTICS")
        print("="*50)
        print(f"Known Faces: {stats['known_faces']}")
        print(f"Unknown Faces: {stats['unknown_faces']}")
        print(f"Admin Face Enrolled: {stats['admin_enrolled']}")
        print(f"ECC Curve: {stats['ecc_curve']}")
        print(f"Public Key: {stats['public_key']}")
    
    def list_known_faces(self):
        """List all known faces"""
        faces = self.manager.list_known_faces()
        print(f"\n{'='*50}")
        print(f"KNOWN FACES DATABASE ({len(faces)})")
        print("="*50)
        if faces:
            for i, face in enumerate(faces, 1):
                print(f"{i}. {face}")
        else:
            print("No known faces. Add images to src/facebase/known_faces/")
    
    def list_unknown_faces(self):
        """List all unknown faces"""
        faces = self.manager.list_unknown_faces()
        print(f"\n{'='*50}")
        print(f"UNKNOWN FACES ({len(faces)})")
        print("="*50)
        if faces:
            for i, face in enumerate(faces, 1):
                print(f"{i}. {face}")
        else:
            print("No unknown faces captured yet")
    
    def add_unknown_to_known(self):
        """Add unknown face to known database"""
        unknowns = self.manager.list_unknown_faces()
        if not unknowns:
            print("No unknown faces available")
            return
        
        self.list_unknown_faces()
        try:
            idx = int(input("\nSelect face number: ")) - 1
            if 0 <= idx < len(unknowns):
                name = input("Enter person's name: ").strip().replace(' ', '_')
                if self.manager.add_face_to_known(unknowns[idx], name):
                    print(f"✓ Added {name} to known faces database")
                else:
                    print("✗ Failed to add face")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    
    def change_password(self):
        """Change admin password"""
        print("\n" + "="*50)
        print("CHANGE PASSWORD")
        print("="*50)
        old = getpass.getpass("Old password: ")
        new = getpass.getpass("New password: ")
        confirm = getpass.getpass("Confirm new password: ")
        
        if new != confirm:
            print("✗ Passwords don't match")
            return
        
        if self.manager.change_password(old, new):
            print("✓ Password changed successfully")
            print("✓ Data re-encrypted with ECC")
        else:
            print("✗ Failed to change password")
    
    def show_public_key(self):
        """Show ECC public key"""
        print("\n" + "="*50)
        print("ECC PUBLIC KEY (SECP256k1)")
        print("="*50)
        print(f"Address: {self.manager.storage.get_public_key_address()}")
        print("Curve: SECP256k1 (Bitcoin Standard)")
        print("Hash: SHA256 + RIPEMD160")
    
    def analyze_face_deepface(self):
        """Analyze a face using DeepFace"""
        faces = self.manager.list_unknown_faces() + self.manager.list_known_faces()
        if not faces:
            print("No faces available for analysis")
            return
        
        print("\nAvailable faces:")
        for i, face in enumerate(faces, 1):
            print(f"{i}. {face}")
        
        try:
            idx = int(input("\nSelect face to analyze: ")) - 1
            if 0 <= idx < len(faces):
                # Determine path
                if faces[idx] in self.manager.list_unknown_faces():
                    path = os.path.join("src/facebase/unknown_faces", faces[idx])
                else:
                    path = os.path.join("src/facebase/known_faces", faces[idx])
                
                print("\nAnalyzing with DeepFace...")
                provider = DeepFaceProvider()
                result = provider.analyze_face(path)
                
                print("\n" + "="*50)
                print("DEEPFACE ANALYSIS")
                print("="*50)
                if 'error' in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Age: {result.get('age', 'N/A')}")
                    print(f"Gender: {result.get('gender', 'N/A')}")
                    print(f"Emotion: {result.get('emotion', 'N/A')}")
                    print(f"Race: {result.get('race', 'N/A')}")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Analysis failed: {e}")
    
    def test_ai(self):
        """Test AI integration"""
        print("\n" + "="*50)
        print("AI INTEGRATION TEST")
        print("="*50)
        print("1. Test OpenAI (requires API key)")
        print("2. Test DeepFace")
        print("3. Test Mock AI")
        
        choice = input("\nSelect provider: ").strip()
        
        if choice == '1':
            api_key = input("Enter OpenAI API key (or press Enter to skip): ").strip()
            adapter = AIAdapter("openai", api_key if api_key else None)
        elif choice == '2':
            adapter = AIAdapter("deepface")
        else:
            adapter = AIAdapter("mock")
        
        # Test event processing
        test_event = {
            'type': 'new_face',
            'name': 'Test Subject',
            'confidence': 0.95,
            'timestamp': '2024-01-01T12:00:00'
        }
        
        print("\nProcessing test event...")
        result = adapter.analyze(test_event)
        print(f"Result: {result}")
        
        # Test summary
        test_events = [
            "[12:00:00] New face detected: Person A",
            "[12:05:00] New face detected: Person B",
            "[12:10:00] Unknown face detected"
        ]
        
        print("\nGenerating summary...")
        summary = adapter.summarize(test_events)
        print(f"Summary: {summary}")
