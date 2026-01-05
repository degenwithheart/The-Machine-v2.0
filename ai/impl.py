"""AI implementation with multiple provider support"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_core import MockAIProvider
from src.ai_adapters import OpenAIProvider, DeepFaceProvider

class AIImplementation:
    """
    Main AI implementation class supporting multiple providers
    """
    
    def __init__(self, provider_type="mock", api_key=None):
        self.provider_type = provider_type
        self.provider = self._initialize_provider(provider_type, api_key)
    
    def _initialize_provider(self, provider_type, api_key):
        """Initialize the specified AI provider"""
        if provider_type == "openai":
            return OpenAIProvider(api_key)
        elif provider_type == "deepface":
            return DeepFaceProvider()
        else:
            return MockAIProvider()
    
    def analyze_surveillance_event(self, event):
        """Analyze surveillance event"""
        return self.provider.process_event(event)
    
    def analyze_face_attributes(self, image_path):
        """Analyze face attributes (best with DeepFace)"""
        return self.provider.analyze_face(image_path)
    
    def generate_report(self, events):
        """Generate event report"""
        return self.provider.generate_summary(events)

# Example usage
if __name__ == "__main__":
    print("Testing AI Implementation...")
    
    # Test Mock Provider
    print("\n1. Testing Mock Provider:")
    ai = AIImplementation("mock")
    test_event = {'type': 'new_face', 'name': 'Test Person', 'confidence': 0.95}
    print(ai.analyze_surveillance_event(test_event))
    
    # Test OpenAI (if available)
    print("\n2. Testing OpenAI Provider:")
    ai_openai = AIImplementation("openai")
    print(ai_openai.analyze_surveillance_event(test_event))
    
    # Test DeepFace
    print("\n3. Testing DeepFace Provider:")
    ai_deepface = AIImplementation("deepface")
    print("DeepFace requires image path for analysis")
