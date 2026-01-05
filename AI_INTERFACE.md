# AI Interface Documentation

## Overview

The Machine v2.0 uses a modular AI interface system that supports multiple providers.

## Supported Providers

- **OpenAI GPT** - Text analysis, event summarization, threat assessment
- **DeepFace** - Facial attribute analysis (age, gender, emotion, race)
- **Mock** - Testing and development

## OpenAI Integration

### Setup

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Features

- Event narrative generation
- Threat level assessment
- Behavioral pattern analysis
- Natural language summaries

## DeepFace Integration

### Features

- Age estimation
- Gender detection
- Emotion recognition (angry, fear, neutral, sad, happy, surprise, disgust)
- Race classification
- Face verification

## API Structure

### Face Analysis

```python
analyze_face(image_path: str) -> dict
# Returns: {age, gender, emotion, race, confidence}
```

### Event Processing

```python
process_event(event_data: dict) -> str
# Returns: AI-generated event description
```

### Decision Making

```python
should_alert(face_id: str, confidence: float) -> bool
# Returns: True if alert should be triggered
```

## Usage Examples

```python
# OpenAI Provider
from ai.impl import OpenAIProvider
provider = OpenAIProvider(api_key="your-key")
summary = provider.generate_summary(events)

# DeepFace Provider
from ai.impl import DeepFaceProvider
provider = DeepFaceProvider()
analysis = provider.analyze_face("path/to/face.jpg")
```
