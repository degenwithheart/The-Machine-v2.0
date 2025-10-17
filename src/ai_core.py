"""
AI core interface module.

This file intentionally contains interface stubs only. The real AI
implementation should be provided in an external `ai/` package dropped in
the repository root. When that package is present `src.ai_loader.get_ai()`
returns it and the external implementation will be used for all AI tasks.

The stubs below make it obvious which functions the external AI must
implement. They raise NotImplementedError so using them without providing
an external AI results in clear failures rather than hidden fake data.

Purpose:
- Define the contract for AI implementations.
- Ensure consistent API across different AI backends.
- Prevent accidental use of incomplete implementations.
- Provide clear error messages when AI is missing.

Implementation Notes:
- All functions should be thread-safe where possible.
- Handle image formats: JPEG, PNG bytes.
- Return types must match exactly.
- Raise exceptions on fatal errors, not on recoverable issues.
"""

from typing import Any, Dict, List


def generate_embedding(data: bytes, dim: int = 512) -> List[float]:
    """
    Generate a numerical embedding vector from face image bytes.

    This function extracts a fixed-size feature vector representing the face,
    used for similarity matching and identification.

    Args:
        data: Raw image bytes (JPEG/PNG) containing a face.
        dim: Expected dimension of the embedding vector (default 512).

    Returns:
        List of floats representing the face embedding.

    Raises:
        NotImplementedError: If not implemented by external AI.
        Exception: On processing errors (e.g., no face detected).

    Notes:
        - Vector size should be consistent across calls.
        - Optimized for speed in real-time applications.
        - Supports single face per image.
    """
    raise NotImplementedError("generate_embedding must be implemented by external AI")


def match_embedding(embedding: List[float], candidates: Dict[str, List[float]], threshold: float = 0.8):
    """
    Match a query embedding against a database of candidate embeddings.

    Finds the best matching candidate based on similarity score.

    Args:
        embedding: Query embedding vector to match.
        candidates: Dict mapping IDs to their embedding vectors.
        threshold: Minimum similarity score for a valid match (0.0-1.0).

    Returns:
        Tuple of (matched_id: str or None, score: float).
        - matched_id: ID of best match, or None if no match above threshold.
        - score: Similarity score of the match.

    Raises:
        NotImplementedError: If not implemented by external AI.
        Exception: On computation errors.

    Notes:
        - Score closer to 1.0 indicates higher similarity.
        - Efficient for large candidate sets (consider indexing).
        - Thread-safe for concurrent matching.
    """
    raise NotImplementedError("match_embedding must be implemented by external AI")


def analyze_attributes(data: bytes) -> Dict[str, Any]:
    """
    Analyze facial attributes from image bytes.

    Extracts demographic and emotional information from detected faces.

    Args:
        data: Raw image bytes (JPEG/PNG) containing a face.

    Returns:
        Dict with attribute keys, e.g.:
        {
            "age": 25,
            "gender": "female",
            "dominant_emotion": "happy",
            "race": "asian"
        }

    Raises:
        NotImplementedError: If not implemented by external AI.
        Exception: On analysis errors.

    Notes:
        - Return empty dict if analysis fails.
        - Values can be strings, numbers, or nested structures.
        - Supports single face per image.
    """
    raise NotImplementedError("analyze_attributes must be implemented by external AI")


def predict_violent_event(event: Dict[str, Any]) -> float:
    """
    Predict the risk of a violent event from surveillance data.

    Analyzes event metadata to assess potential threat level.

    Args:
        event: Dict containing event data, e.g.:
        {
            "faces": 2,
            "motion": True,
            "description": "fight in hallway",
            "location": "entrance"
        }

    Returns:
        Float risk score between 0.0 (no risk) and 1.0 (high risk).

    Raises:
        NotImplementedError: If not implemented by external AI.
        Exception: On prediction errors.

    Notes:
        - Use features like face count, motion detection, text analysis.
        - Fast for real-time processing.
        - Calibrated for false positive minimization.
    """
    raise NotImplementedError("predict_violent_event must be implemented by external AI")


def classify_relevance(event: Dict[str, Any]) -> str:
    """
    Classify if an event is relevant for surveillance attention.

    Determines whether the event warrants logging or alerting.

    Args:
        event: Dict with surveillance event data.

    Returns:
        "relevant" or "irrelevant" string.

    Raises:
        NotImplementedError: If not implemented by external AI.
        Exception: On classification errors.

    Notes:
        - Binary classification for quick filtering.
        - Based on event features (faces, motion, etc.).
        - Low computational overhead.
    """
    raise NotImplementedError("classify_relevance must be implemented by external AI")


def ingest_stream(event: Dict[str, Any], store_path: str = "facebase/stream_events.json") -> Dict[str, Any]:
    """
    Process and store a streaming surveillance event with AI analysis.

    Analyzes the event, stores it persistently, and returns analysis results.

    Args:
        event: Dict with live event data from streams.
        store_path: File path to append event JSON.

    Returns:
        Dict with analysis results, e.g.:
        {
            "score": 0.7,
            "relevance": "relevant",
            "attributes": {...}
        }

    Raises:
        NotImplementedError: If not implemented by external AI.
        Exception: On processing or storage errors.

    Notes:
        - Appends to JSON file for persistence.
        - Includes I/O operations; may be slow.
        - Returns serializable dict for logging.
    """
    raise NotImplementedError("ingest_stream must be implemented by external AI")

from typing import Any, Dict, List


def generate_embedding(data: bytes, dim: int = 512) -> List[float]:
    raise NotImplementedError("generate_embedding must be implemented by external AI")


def match_embedding(embedding: List[float], candidates: Dict[str, List[float]], threshold: float = 0.8):
    raise NotImplementedError("match_embedding must be implemented by external AI")


def analyze_attributes(data: bytes) -> Dict[str, Any]:
    raise NotImplementedError("analyze_attributes must be implemented by external AI")


def predict_violent_event(event: Dict[str, Any]) -> float:
    raise NotImplementedError("predict_violent_event must be implemented by external AI")


def classify_relevance(event: Dict[str, Any]) -> str:
    raise NotImplementedError("classify_relevance must be implemented by external AI")


def ingest_stream(event: Dict[str, Any], store_path: str = "facebase/stream_events.json"):
    raise NotImplementedError("ingest_stream must be implemented by external AI")
