"""AI API wrappers for OpenAI and DeepFace"""
import os
import sys
from src.ai_core import AIProvider, MockAIProvider

class OpenAIProvider(AIProvider):
    """OpenAI GPT integration for event analysis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not set. Using mock responses.")
            self.enabled = False
        else:
            self.enabled = True
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                print("✓ OpenAI provider initialized")
            except ImportError:
                print("Warning: openai package not installed. Run: pip install openai")
                self.enabled = False
            except Exception as e:
                print(f"Warning: OpenAI initialization failed: {e}")
                self.enabled = False
    
    def analyze_face(self, image_path):
        """OpenAI doesn't do face analysis - delegate to DeepFace"""
        return {"note": "Use DeepFace for facial analysis"}
    
    def process_event(self, event_data):
        """Process surveillance event with GPT analysis"""
        if not self.enabled:
            return f"[Mock] Detected {event_data.get('name', 'Unknown')}"
        
        try:
            prompt = f"""Analyze this surveillance event briefly (one sentence):
Event: {event_data.get('type')}
Person: {event_data.get('name', 'Unknown')}
Confidence: {event_data.get('confidence', 0):.2%}
Time: {event_data.get('timestamp')}

Provide a security assessment."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a security analyst. Respond in one brief sentence."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI Error: {str(e)[:50]}]"
    
    def generate_summary(self, events):
        """Generate narrative summary of multiple events"""
        if not self.enabled or not events:
            return f"Mock summary: {len(events)} events recorded"
        
        try:
            event_list = "\n".join([f"- {e}" for e in events[-10:]])
            
            prompt = f"""Summarize these surveillance events in 2-3 sentences:

{event_list}

Provide an executive security summary."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a security analyst. Be concise."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Summary generation failed: {str(e)[:100]}"


class DeepFaceProvider(AIProvider):
    """DeepFace integration for facial attribute analysis"""
    
    def __init__(self):
        try:
            from deepface import DeepFace
            self.DeepFace = DeepFace
            self.enabled = True
            print("✓ DeepFace provider initialized")
        except ImportError:
            print("Warning: deepface not installed. Run: pip install deepface")
            self.enabled = False
        except Exception as e:
            print(f"Warning: DeepFace init failed: {e}")
            self.enabled = False
    
    def analyze_face(self, image_path):
        """Analyze facial attributes: age, gender, emotion, race"""
        if not self.enabled:
            return {"status": "DeepFace not available"}
        
        if not os.path.exists(image_path):
            return {"error": "Image not found"}
        
        try:
            analysis = self.DeepFace.analyze(
                img_path=image_path,
                actions=['age', 'gender', 'emotion', 'race'],
                enforce_detection=False,
                silent=True
            )
            
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            return {
                "age": analysis.get('age', 'unknown'),
                "gender": analysis.get('dominant_gender', 'unknown'),
                "emotion": analysis.get('dominant_emotion', 'unknown'),
                "race": analysis.get('dominant_race', 'unknown'),
                "confidence": {
                    "emotion": analysis.get('emotion', {}),
                    "gender": analysis.get('gender', {}),
                    "race": analysis.get('race', {})
                }
            }
        except Exception as e:
            return {"error": str(e)[:100]}
    
    def process_event(self, event_data):
        """Process event with face analysis"""
        return f"Face detected: {event_data.get('name', 'Unknown')}"
    
    def generate_summary(self, events):
        """Generate summary"""
        return f"DeepFace analyzed {len(events)} face detection events"
    
    def verify_faces(self, img1_path, img2_path):
        """Verify if two faces are the same person"""
        if not self.enabled:
            return {"verified": False, "message": "DeepFace not available"}
        
        try:
            result = self.DeepFace.verify(
                img1_path=img1_path,
                img2_path=img2_path,
                enforce_detection=False
            )
            return result
        except Exception as e:
            return {"error": str(e), "verified": False}


class AIAdapter:
    """Main AI adapter that can use multiple providers"""
    
    def __init__(self, provider_name="mock", api_key=None):
        self.provider_name = provider_name
        self.provider = self._load_provider(provider_name, api_key)
    
    def _load_provider(self, name, api_key=None):
        """Load AI provider safely"""
        try:
            if name == "openai":
                return OpenAIProvider(api_key)
            elif name == "deepface":
                return DeepFaceProvider()
            elif name == "mock":
                return MockAIProvider()
            else:
                print(f"Provider '{name}' not found, using mock")
                return MockAIProvider()
        except Exception as e:
            print(f"Error loading provider: {e}")
            return MockAIProvider()
    
    def analyze(self, data):
        """Safe analysis wrapper"""
        try:
            if isinstance(data, dict) and 'type' in data:
                return self.provider.process_event(data)
            elif isinstance(data, str):
                return self.provider.analyze_face(data)
            else:
                return "Unknown data type"
        except Exception as e:
            print(f"Analysis error: {e}")
            return f"Error: {str(e)[:50]}"
    
    def summarize(self, events):
        """Generate event summary"""
        try:
            return self.provider.generate_summary(events)
        except Exception as e:
            return f"Summary error: {str(e)[:50]}"
