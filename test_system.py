"""Quick system test"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

print("="*60)
print("Testing The Machine v2.0 Components")
print("="*60)
print("")

# Test imports
tests_passed = 0
tests_total = 0

def test_module(name, import_statement):
    global tests_passed, tests_total
    tests_total += 1
    try:
        exec(import_statement)
        print(f"✓ {name}")
        tests_passed += 1
        return True
    except Exception as e:
        print(f"✗ {name}: {e}")
        return False

# Core modules
test_module("Secure Storage (ECC)", "from secure_storage import ECCSecureStorage")
test_module("Face Recognition", "from face_recognition import FaceRecognitionEngine")
test_module("Face Tracking", "from face_tracking import FaceTracker")
test_module("Admin Manager", "from admin import AdminManager")
test_module("Admin Interface", "from admin_clean import AdminInterface")

# AI modules
test_module("AI Core", "from ai_core import MockAIProvider")
test_module("AI Adapters", "from ai_adapters import AIAdapter, OpenAIProvider, DeepFaceProvider")
test_module("AI Hooks", "from ai_hooks import AIHooks")
test_module("AI Loader", "from ai_loader import AILoader")

# Main entry
test_module("Main System", "from main import TheMachine")

print("")
print("="*60)
print(f"Test Results: {tests_passed}/{tests_total} passed")
print("="*60)

if tests_passed == tests_total:
    print("\n✓ All systems operational!")
    print("\nNext steps:")
    print("  1. Add face images to src/facebase/known_faces/")
    print("  2. Run: python src/main.py")
    print("  3. Access Admin Panel to configure")
else:
    print("\n⚠️  Some components failed to load")
    print("Run: pip install -r requirements.txt")
