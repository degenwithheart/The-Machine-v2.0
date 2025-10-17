# AI Integration Interface for The Machine

## Overview
This document defines the comprehensive API that external AI implementations must follow to integrate seamlessly with The Machine surveillance system. The interface ensures modularity, allowing drop-in AI replacements without modifying core system code.

## Goal
- Provide a standardized, minimal API for AI functionality.
- Enable immediate use of AI capabilities across admin, face recognition, and streaming components.
- Support both simple verification and advanced features like sentiment analysis and adaptive learning.
- Ensure thread-safety and performance for real-time surveillance operations.

## Placement
Place your AI implementation in the repository root under a directory named `ai`. The system supports two loading methods:

### Method 1: Package Structure
```
ai/
  __init__.py  # Exports all required functions
  impl.py      # Actual implementation (optional)
```

### Method 2: Single Module
```
ai/
  impl.py      # Contains all functions, loaded directly
```

**Note**: The loader (`src/ai_loader.py`) attempts package import first, then falls back to `impl.py`.

## Required Functions

### Core Facial Authentication APIs

#### Preferred Single-Call Verification
- `verify_face(live_image_bytes: bytes, reference_image_bytes: bytes) -> bool`
  - **Purpose**: Direct comparison of live vs. reference face images.
  - **Input**: Raw JPEG/PNG bytes for both images.
  - **Output**: Boolean indicating match (True) or no match (False).
  - **Behavior**: Should be deterministic, raising exceptions only for fatal errors like corrupted data.
  - **Performance**: Optimize for speed; used in authentication flows.

#### Alternative Embedding-Based Verification
- `generate_embedding(image_bytes: bytes) -> List[float]`
  - **Purpose**: Extract numerical representation (embedding) from face image.
  - **Input**: Raw image bytes.
  - **Output**: Fixed-size list of floats (e.g., 128 or 512 dimensions).
  - **Behavior**: Consistent vector size across calls; handles various image formats.
  - **Performance**: May be computationally intensive; cache results when possible.

- `match_embedding(embedding: List[float], candidates: Dict[str, List[float]], threshold: float = 0.8) -> Tuple[Optional[str], float]`
  - **Purpose**: Find best matching candidate from a database of embeddings.
  - **Input**: Query embedding, dict of {id: embedding}, similarity threshold.
  - **Output**: (best_match_id or None, confidence_score).
  - **Behavior**: Returns None if no match exceeds threshold; score indicates similarity strength.
  - **Performance**: Efficient for large candidate sets; consider indexing for scalability.

- `analyze_attributes(image_bytes: bytes) -> Dict[str, Any]`
  - **Purpose**: Extract demographic and emotional attributes from face.
  - **Input**: Raw image bytes.
  - **Output**: Dict with keys like 'age', 'gender', 'dominant_emotion', 'race'.
  - **Behavior**: Return empty dict if analysis fails; values can be strings, numbers, or lists.
  - **Performance**: Moderate computation; used for logging and profiling.

### Streaming and Event Analysis APIs

- `predict_violent_event(event: Dict[str, Any]) -> float`
  - **Purpose**: Assess risk of violent activity in surveillance events.
  - **Input**: Event dict containing metadata (e.g., {'faces': 2, 'motion': True, 'description': 'fight'}).
  - **Output**: Risk score from 0.0 (no risk) to 1.0 (high risk).
  - **Behavior**: Use event features like face count, motion detection, text analysis.
  - **Performance**: Fast for real-time processing.

- `classify_relevance(event: Dict[str, Any]) -> str`
  - **Purpose**: Determine if event warrants attention.
  - **Input**: Event dict with surveillance data.
  - **Output**: 'relevant' or 'irrelevant'.
  - **Behavior**: Binary classification; 'relevant' triggers logging/alerts.
  - **Performance**: Lightweight; called frequently in streaming.

- `ingest_stream(event: Dict[str, Any], store_path: str = "facebase/stream_events.json") -> Dict[str, Any]`
  - **Purpose**: Process and store streaming events with AI analysis.
  - **Input**: Event dict, optional storage path.
  - **Output**: Analysis dict (e.g., {'score': 0.7, 'relevance': 'relevant', 'attributes': {...}}).
  - **Behavior**: Append to JSON file; return serializable results.
  - **Performance**: Includes I/O; consider async for high-throughput streams.

### Surveillance Control APIs

- `start_passive_monitoring() -> None`
  - **Purpose**: Initiate background logging of events without active intervention.
  - **Behavior**: Runs indefinitely until stopped; logs to files/databases.
  - **Integration**: Called from admin menu or CLI flags.

- `start_active_alerts() -> None`
  - **Purpose**: Enable real-time alerts on detections (e.g., email, notifications).
  - **Behavior**: Monitors streams, triggers notifications; may include audio/visual cues.
  - **Integration**: Escalates from passive mode.

- `start_event_detection() -> None`
  - **Purpose**: Full autonomous detection and response (e.g., lock doors, call authorities).
  - **Behavior**: Advanced mode with decision-making; requires high confidence.
  - **Integration**: Highest surveillance level.

- `stop_surveillance() -> None`
  - **Purpose**: Halt all active surveillance modes.
  - **Behavior**: Clean shutdown; saves state if needed.
  - **Integration**: Universal stop command.

- `detect_intrusion(image_bytes: bytes) -> Dict[str, Any]`
  - **Purpose**: Analyze images for unauthorized presence.
  - **Input**: Image bytes from cameras.
  - **Output**: {'intrusion': bool, 'confidence': float, 'details': {...}}.
  - **Behavior**: Combines face detection with anomaly analysis.
  - **Performance**: Real-time capable.

- `log_ai_event(message: str) -> None`
  - **Purpose**: Record AI-specific events or decisions.
  - **Input**: Descriptive message string.
  - **Behavior**: Appends to AI log file; may include timestamps/metadata.
  - **Integration**: Used internally by AI for self-reporting.

### Advanced AI Features

- `analyze_sentiment(text: str) -> Dict[str, float]`
  - **Purpose**: Gauge emotional tone in text (logs, conversations).
  - **Input**: Text string (e.g., event descriptions).
  - **Output**: {'positive': 0.6, 'negative': 0.2, 'neutral': 0.2}.
  - **Behavior**: Multi-class sentiment; scores sum to ~1.0.
  - **Performance**: NLP-intensive; cache for repeated text.

- `detect_threat(text: str) -> Dict[str, Any]`
  - **Purpose**: Identify potential threats in text.
  - **Input**: Text to analyze.
  - **Output**: {'threat_level': 'high', 'keywords': ['weapon'], 'confidence': 0.9}.
  - **Behavior**: Keyword-based with ML enhancement; levels: low/medium/high.
  - **Performance**: Fast for security scanning.

- `detect_sarcasm(text: str) -> float`
  - **Purpose**: Detect sarcastic intent to avoid misinterpretation.
  - **Input**: Text string.
  - **Output**: Probability from 0.0 (not sarcastic) to 1.0 (highly sarcastic).
  - **Behavior**: Contextual analysis; useful for conversational AI.
  - **Performance**: Moderate; may use heuristics.

- `generate_response(prompt: str) -> str`
  - **Purpose**: Create natural language responses in conversations.
  - **Input**: User prompt or query.
  - **Output**: AI-generated reply string.
  - **Behavior**: Context-aware; handles greetings, commands, questions.
  - **Performance**: Variable; may involve generation models.

- `synthesize_audio(text: str) -> bytes`
  - **Purpose**: Convert text responses to speech audio.
  - **Input**: Text string.
  - **Output**: Audio bytes (e.g., WAV/MP3).
  - **Behavior**: Returns raw audio data; system handles playback.
  - **Performance**: Computationally heavy; cache common phrases.

- `retrain_model(data: List[Dict[str, Any]], schedule: str = "daily") -> None`
  - **Purpose**: Update AI models with new training data.
  - **Input**: List of training samples, retraining frequency.
  - **Output**: None (side effect: updated model).
  - **Behavior**: Scheduled retraining; data format depends on model.
  - **Performance**: Background task; may take hours.

- `self_monitor() -> Dict[str, Any]`
  - **Purpose**: Report AI system health and resource usage.
  - **Output**: {'cpu': 45.0, 'memory': 512, 'performance': 0.9, 'errors': 0}.
  - **Behavior**: Real-time metrics; used for adaptive adjustments.
  - **Performance**: Lightweight polling.

- `adaptive_learn(feedback: Dict[str, Any]) -> None`
  - **Purpose**: Adjust AI behavior based on user/system feedback.
  - **Input**: Feedback dict (e.g., {'action': 'increase_threshold', 'reason': 'false_positives'}).
  - **Behavior**: Modifies parameters like detection thresholds.
  - **Performance**: Quick updates; persists changes.

## Integration Behavior
- **Dynamic Loading**: System imports `ai` module at runtime; functions are called via `ai_loader.get_ai()`.
- **Fallback Handling**: If AI unavailable, system degrades gracefully (e.g., no embeddings, basic logging).
- **Pending Processing**: `face_recognition.process_pending()` invokes `generate_embedding` and `analyze_attributes` on each file in `facebase/pending/`, then registers results.
- **Authentication Flow**: Prefers `verify_face`; falls back to embedding pipeline.
- **Event Streaming**: Hooks in `ai_hooks.py` call `ingest_stream` for real-time analysis.

## Threading and Performance Considerations
- **Concurrency**: Functions may be called from multiple threads; ensure thread-safety (e.g., no shared mutable state).
- **Optimization**: `generate_embedding` and `analyze_attributes` are hot paths; use GPU acceleration if available.
- **Async Support**: For high-load scenarios, consider async versions or queue-based processing.
- **Resource Limits**: Monitor memory usage; large models may require unloading when idle.

## Error Handling Guidelines
- **Exceptions**: Raise on irrecoverable errors (e.g., invalid input, model failure); system catches and retries later.
- **Graceful Degradation**: Return defaults (e.g., empty dict, None) for recoverable issues.
- **Logging**: Use `log_ai_event` for internal diagnostics; avoid print statements.

## Usage Examples
- **Face Verification**: `ai.verify_face(live_bytes, ref_bytes)` → True/False
- **Embedding Match**: `emb = ai.generate_embedding(img); match, score = ai.match_embedding(emb, db)`
- **Sentiment Analysis**: `scores = ai.analyze_sentiment("Great job!")` → {'positive': 0.9}
- **Threat Detection**: `threat = ai.detect_threat("Bomb threat")` → {'threat_level': 'high'}

## Example Skeleton Implementation
Refer to `ai/impl.py` for a starting template. Replace `NotImplementedError` with actual logic using your preferred ML frameworks (TensorFlow, PyTorch, etc.).

## Versioning and Compatibility
- API is stable; additions are backward-compatible.
- Future versions may add optional parameters or new functions.
- Test implementations against the system's integration points.
