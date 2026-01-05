"""Real-time face tracking and monitoring with AI integration"""
import cv2
import time
import os
from datetime import datetime

class FaceTracker:
    def __init__(self, recognition_engine, ai_adapter=None):
        self.engine = recognition_engine
        self.ai_adapter = ai_adapter
        self.tracked_faces = {}
        self.events = []
        self.frame_count = 0
        self.unknown_save_interval = 30  # Save unknown faces every 30 frames
    
    def process_frame(self, frame):
        """Process single frame and track faces"""
        self.frame_count += 1
        results = self.engine.recognize_faces(frame)
        timestamp = datetime.now()
        
        for result in results:
            name = result['name']
            confidence = result['confidence']
            location = result['location']
            
            # Draw rectangle and label
            top, right, bottom, left = location
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            label = f"{name}"
            if confidence > 0:
                label += f" ({confidence:.2%})"
            
            cv2.putText(frame, label, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            # Track event
            if name not in self.tracked_faces:
                self.tracked_faces[name] = {
                    'first_seen': timestamp,
                    'last_seen': timestamp,
                    'count': 1,
                    'total_confidence': confidence
                }
                self.log_event(f"NEW: {name} detected (confidence: {confidence:.2%})")
                
                # Save unknown face
                if name == "Unknown" and self.frame_count % self.unknown_save_interval == 0:
                    filename = self.engine.save_unknown_face(frame, location)
                    self.log_event(f"Saved unknown face: {filename}")
                
                # AI event processing
                if self.ai_adapter:
                    event_data = {
                        'type': 'new_face',
                        'name': name,
                        'confidence': confidence,
                        'timestamp': timestamp.isoformat(),
                        'location': location
                    }
                    try:
                        ai_response = self.ai_adapter.analyze(event_data)
                        if ai_response and isinstance(ai_response, str):
                            self.log_event(f"AI: {ai_response}")
                    except Exception as e:
                        self.log_event(f"AI Error: {e}")
            else:
                self.tracked_faces[name]['last_seen'] = timestamp
                self.tracked_faces[name]['count'] += 1
                self.tracked_faces[name]['total_confidence'] += confidence
        
        # Add info overlay
        self._draw_info_overlay(frame)
        
        return frame, results
    
    def _draw_info_overlay(self, frame):
        """Draw information overlay on frame"""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # System info
        cv2.putText(frame, "THE MACHINE v2.0", (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Tracking: {len(self.tracked_faces)} faces", (20, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Events: {len(self.events)}", (20, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        ai_status = "AI: Active" if self.ai_adapter else "AI: Offline"
        color = (0, 255, 0) if self.ai_adapter else (0, 0, 255)
        cv2.putText(frame, ai_status, (20, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def log_event(self, message):
        """Log system event"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"[{timestamp}] {message}"
        self.events.append(event)
        print(event)
        
        # Keep only last 1000 events in memory
        if len(self.events) > 1000:
            self.events = self.events[-1000:]
    
    def get_stats(self):
        """Get tracking statistics"""
        stats = {
            'total_faces': len(self.tracked_faces),
            'events': len(self.events),
            'tracked': {}
        }
        
        for name, data in self.tracked_faces.items():
            avg_confidence = data['total_confidence'] / data['count']
            stats['tracked'][name] = {
                'first_seen': data['first_seen'].strftime("%Y-%m-%d %H:%M:%S"),
                'last_seen': data['last_seen'].strftime("%Y-%m-%d %H:%M:%S"),
                'detections': data['count'],
                'avg_confidence': f"{avg_confidence:.2%}"
            }
        
        return stats
    
    def save_events_log(self, filename="surveillance_log.txt"):
        """Save events to file"""
        try:
            with open(filename, 'w') as f:
                f.write("THE MACHINE v2.0 - Surveillance Log\n")
                f.write("=" * 60 + "\n\n")
                for event in self.events:
                    f.write(event + "\n")
            print(f"Events saved to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save events: {e}")
            return False
