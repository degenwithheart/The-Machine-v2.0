"""Face recognition engine"""
import os
import cv2
import face_recognition
import numpy as np
from pathlib import Path

class FaceRecognitionEngine:
    def __init__(self, known_faces_dir="src/facebase/known_faces"):
        self.known_faces_dir = known_faces_dir
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load all known faces from directory"""
        self.known_encodings = []
        self.known_names = []
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir, exist_ok=True)
            print("No known faces found. Add images to src/facebase/known_faces/")
            return
        
        for filename in os.listdir(self.known_faces_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                path = os.path.join(self.known_faces_dir, filename)
                try:
                    image = face_recognition.load_image_file(path)
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        self.known_encodings.append(encodings[0])
                        name = os.path.splitext(filename)[0].replace('_', ' ').title()
                        self.known_names.append(name)
                        print(f"  Loaded: {name}")
                except Exception as e:
                    print(f"  Error loading {filename}: {e}")
        
        print(f"Total known faces loaded: {len(self.known_names)}")
    
    def recognize_faces(self, frame):
        """Detect and recognize faces in frame"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        results = []
        for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            name = "Unknown"
            confidence = 0.0
            
            if self.known_encodings:
                distances = face_recognition.face_distance(self.known_encodings, encoding)
                best_match_idx = np.argmin(distances)
                
                if distances[best_match_idx] < 0.6:
                    name = self.known_names[best_match_idx]
                    confidence = 1.0 - distances[best_match_idx]
            
            results.append({
                'name': name,
                'confidence': confidence,
                'location': (top, right, bottom, left),
                'encoding': encoding
            })
        
        return results
    
    def save_unknown_face(self, frame, location):
        """Save unknown face for later identification"""
        top, right, bottom, left = location
        # Add padding
        padding = 20
        top = max(0, top - padding)
        left = max(0, left - padding)
        bottom = min(frame.shape[0], bottom + padding)
        right = min(frame.shape[1], right + padding)
        
        face_img = frame[top:bottom, left:right]
        
        unknown_dir = "src/facebase/unknown_faces"
        os.makedirs(unknown_dir, exist_ok=True)
        
        count = len([f for f in os.listdir(unknown_dir) if f.startswith('unknown_')])
        filename = f"unknown_{count+1}.jpg"
        filepath = os.path.join(unknown_dir, filename)
        cv2.imwrite(filepath, face_img)
        return filename
