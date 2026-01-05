"""Main entry point and CLI interface"""
import cv2
import sys
import os
import time
from face_recognition import FaceRecognitionEngine
from face_tracking import FaceTracker
from admin_clean import AdminInterface
from ai_adapters import AIAdapter

class TheMachine:
    def __init__(self):
        print("\nInitializing The Machine v2.0...")
        self.engine = FaceRecognitionEngine()
        self.ai_adapter = None
        self.tracker = None
        self.admin = AdminInterface()
        self.running = False
    
    def initialize_ai(self, provider="mock", api_key=None):
        """Initialize AI provider"""
        print(f"\nInitializing AI provider: {provider}")
        self.ai_adapter = AIAdapter(provider, api_key)
        self.tracker = FaceTracker(self.engine, self.ai_adapter)
        print("✓ AI integration ready")
    
    def camera_mode(self):
        """Start camera surveillance"""
        if not self.tracker:
            self.initialize_ai("mock")
        
        print("\n" + "="*60)
        print("CAMERA MODE - Live Surveillance")
        print("="*60)
        print("Controls:")
        print("  'q' - Quit")
        print("  's' - Save current frame")
        print("  'l' - Save event log")
        print("  'r' - Reload known faces")
        print("="*60)
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Error: Cannot access camera")
            print("Please check:")
            print("  1. Camera is connected")
            print("  2. No other app is using the camera")
            print("  3. Camera permissions are granted")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("✓ Camera initialized")
        print("Starting surveillance...")
        
        self.running = True
        frame_count = 0
        fps_start = time.time()
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process frame
            processed_frame, results = self.tracker.process_frame(frame)
            
            # Calculate FPS
            frame_count += 1
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start)
                cv2.putText(processed_frame, f"FPS: {fps:.1f}", (processed_frame.shape[1] - 150, 35),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                fps_start = time.time()
            
            # Display
            cv2.imshow('The Machine v2.0 - Surveillance', processed_frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nShutting down surveillance...")
                break
            elif key == ord('s'):
                filename = f"capture_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                print(f"✓ Frame saved: {filename}")
            elif key == ord('l'):
                self.tracker.save_events_log()
            elif key == ord('r'):
                print("\nReloading known faces...")
                self.engine.load_known_faces()
        
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Camera mode ended")
    
    def show_stats(self):
        """Display system statistics"""
        if not self.tracker:
            print("No tracking data available. Start camera mode first.")
            return
        
        stats = self.tracker.get_stats()
        print("\n" + "="*60)
        print("SYSTEM STATISTICS")
        print("="*60)
        print(f"Total Faces Tracked: {stats['total_faces']}")
        print(f"Total Events Logged: {stats['events']}")
        
        if stats['tracked']:
            print("\nDetailed Face Tracking:")
            print("-" * 60)
            for name, data in stats['tracked'].items():
                print(f"\n{name}:")
                print(f"  First Seen: {data['first_seen']}")
                print(f"  Last Seen: {data['last_seen']}")
                print(f"  Detections: {data['detections']}")
                print(f"  Avg Confidence: {data['avg_confidence']}")
        
        print("\n" + "="*60)
    
    def configure_ai(self):
        """Configure AI integration"""
        print("\n" + "="*60)
        print("AI CONFIGURATION")
        print("="*60)
        print("1. Use Mock AI (Testing)")
        print("2. Use OpenAI GPT (Requires API key)")
        print("3. Use DeepFace (Facial Analysis)")
        print("4. Back")
        
        choice = input("\nSelect AI provider: ").strip()
        
        if choice == '1':
            self.initialize_ai("mock")
        elif choice == '2':
            api_key = input("Enter OpenAI API key: ").strip()
            if api_key:
                self.initialize_ai("openai", api_key)
            else:
                print("No API key provided")
        elif choice == '3':
            self.initialize_ai("deepface")
        elif choice == '4':
            return
    
    def main_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print(" "*15 + "THE MACHINE v2.0")
        print(" "*10 + "AI-Powered Surveillance System")
        print("="*60)
        
        while True:
            print("\n" + "-"*60)
            print("MAIN MENU")
            print("-"*60)
            print("1. Camera Mode (Live Surveillance)")
            print("2. Admin Panel (ECC Secured)")
            print("3. AI Configuration")
            print("4. System Status")
            print("5. Exit")
            print("-"*60)
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.camera_mode()
            elif choice == '2':
                self.admin.show_menu()
            elif choice == '3':
                self.configure_ai()
            elif choice == '4':
                self.show_stats()
            elif choice == '5':
                print("\nShutting down The Machine...")
                print("Stay vigilant.")
                sys.exit(0)
            else:
                print("Invalid option. Please select 1-5.")

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("Booting The Machine v2.0...")
        print("="*60)
        machine = TheMachine()
        machine.main_menu()
    except KeyboardInterrupt:
        print("\n\nEmergency shutdown initiated...")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
