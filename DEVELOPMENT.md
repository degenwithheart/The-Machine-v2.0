# Development Guide

## Architecture

### Core Components

1. **Face Recognition Engine** (`face_recognition.py`)
   - Uses face_recognition library
   - Handles encoding and matching
   - 0.6 distance threshold

2. **Face Tracker** (`face_tracking.py`)
   - Real-time processing
   - Event logging
   - AI integration hooks

3. **Secure Storage** (`secure_storage.py`)
   - SECP256k1 elliptic curve
   - Double SHA256 hashing
   - ECDSA signatures

4. **AI Adapters** (`ai_adapters.py`)
   - Provider abstraction
   - OpenAI integration
   - DeepFace integration

### Adding New AI Provider

```python
# In src/ai_adapters.py

class MyAIProvider(AIProvider):
    def __init__(self, config):
        self.config = config
        # Initialize your AI
    
    def analyze_face(self, image_path):
        # Implement face analysis
        return {"attribute": "value"}
    
    def process_event(self, event_data):
        # Implement event processing
        return "AI response"
    
    def generate_summary(self, events):
        # Implement summarization
        return "Summary text"

# Register in AIAdapter._load_provider()
if name == "myai":
    return MyAIProvider(api_key)
```

### Custom Event Hooks

```python
from src.ai_hooks import AIHooks

def my_callback(data):
    print(f"Event triggered: {data}")

hooks = AIHooks(ai_adapter)
hooks.register_hook('new_face', my_callback)
hooks.trigger('new_face', {'name': 'John'})
```

## Testing

### Unit Tests
```bash
python test_system.py
```

### Manual Testing
```bash
# Test face recognition
python -c "from src.face_recognition import *; eng = FaceRecognitionEngine(); print(eng.known_names)"

# Test ECC storage
python src/secure_storage.py

# Test AI providers
python ai/impl.py
```

## Performance Optimization

### Face Recognition
- Resize frames to 0.25x for processing
- Use 'hog' model (faster than 'cnn')
- Process every Nth frame if needed

### Camera Settings
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
```

## Deployment

### Raspberry Pi
```bash
# Install dependencies
sudo apt-get install cmake libopenblas-dev liblapack-dev
pip install -r requirements.txt

# Optimize
# Use smaller resolution
# Reduce FPS if needed
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

## Security Best Practices

1. **Change default password immediately**
2. **Secure private key file** (chmod 600)
3. **Use strong passwords** (12+ characters)
4. **Regular key rotation**
5. **Audit event logs**

## Contributing

1. Fork repository
2. Create feature branch
3. Add tests
4. Update documentation
5. Submit pull request

## API Reference

See `AI_INTERFACE.md` for complete API documentation.
