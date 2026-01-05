"""AI interface contracts and base classes"""

class AIProvider:
    """Base class for AI providers"""
    
    def analyze_face(self, image_path):
        """Analyze face attributes"""
        raise NotImplementedError
    
    def process_event(self, event_data):
        """Process surveillance event"""
        raise NotImplementedError
    
    def generate_summary(self, events):
        """Generate summary of events"""
        raise NotImplementedError

class MockAIProvider(AIProvider):
    """Mock AI for testing"""
    
    def analyze_face(self, image_path):
        return {"age": "unknown", "gender": "unknown", "emotion": "neutral"}
    
    def process_event(self, event_data):
        event_type = event_data.get('type', 'unknown')
        name = event_data.get('name', 'Unknown')
        confidence = event_data.get('confidence', 0)
        return f"Detected {name} (confidence: {confidence:.2%})"
    
    def generate_summary(self, events):
        if not events:
            return "No events to summarize"
        return f"Surveillance summary: {len(events)} events recorded. System operational."
