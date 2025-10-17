"""
AI adapter helpers to centralize calls into the external AI implementation.

These helpers provide small, well-documented wrappers such as
`verify_face_or_none`, `generate_embedding_safe`, and `match_embedding_safe`.
They handle the case where no AI is present and convert exceptions to
controlled return values so callers don't need to duplicate try/except.

Purpose:
- Centralize AI calls to avoid scattering try/except blocks.
- Provide safe fallbacks when AI is unavailable.
- Enable graceful degradation in surveillance operations.
- Support both direct verification and embedding-based matching.

Usage:
- Call these functions instead of directly accessing ai_loader.get_ai().
- Expect None or default values when AI is not loaded.
- Functions are thread-safe as they don't modify shared state.
"""
from typing import Any, Dict, List, Optional, Tuple
from src import ai_loader


def verify_face_or_none(live_bytes: bytes, ref_bytes: bytes) -> Optional[bool]:
    """
    Safely verify if live face matches reference face using AI.

    Attempts direct verification first, falls back to embedding comparison.
    Returns None if AI unavailable or verification fails.

    Args:
        live_bytes: JPEG/PNG bytes of live face image.
        ref_bytes: JPEG/PNG bytes of reference face image.

    Returns:
        True if match, False if no match, None if AI unavailable or error.
    """
    # Get the AI module, returns None if not loaded
    ai = ai_loader.get_ai()
    if ai is None:
        return None
    try:
        # Try direct verification if available
        if hasattr(ai, 'verify_face'):
            return ai.verify_face(live_bytes, ref_bytes)
        # Fallback: use embedding generation and matching
        if hasattr(ai, 'generate_embedding') and hasattr(ai, 'match_embedding'):
            # Generate embeddings for both images
            emb_live = ai.generate_embedding(live_bytes)
            emb_ref = ai.generate_embedding(ref_bytes)
            # Match live embedding against reference
            mid, score = ai.match_embedding(emb_live, {"ref": emb_ref})
            # Return True if match found (mid not None)
            return mid is not None
    except Exception:
        # Return None on any error to indicate failure
        return None
    # Return None if no suitable AI methods available
    return None


def generate_embedding_safe(image_bytes: bytes) -> Optional[List[float]]:
    """
    Safely generate face embedding from image bytes.

    Returns None if AI unavailable or generation fails.

    Args:
        image_bytes: JPEG/PNG bytes of face image.

    Returns:
        List of floats representing face embedding, or None on failure.
    """
    # Get AI module
    ai = ai_loader.get_ai()
    if ai is None:
        return None
    try:
        # Call AI embedding generation
        return ai.generate_embedding(image_bytes)
    except Exception:
        # Return None on error
        return None


def match_embedding_safe(embedding: List[float], candidates: Dict[str, List[float]], threshold: float = 0.8) -> Tuple[Optional[str], float]:
    """
    Safely match embedding against candidate database.

    Returns (None, 0.0) if AI unavailable or matching fails.

    Args:
        embedding: Query embedding to match.
        candidates: Dict of {id: embedding} for database.
        threshold: Minimum similarity score for match.

    Returns:
        Tuple of (matched_id or None, confidence_score).
    """
    # Get AI module
    ai = ai_loader.get_ai()
    if ai is None:
        return None, 0.0
    try:
        # Call AI matching function
        return ai.match_embedding(embedding, candidates, threshold)
    except Exception:
        # Return default on error
        return None, 0.0


def analyze_attributes_safe(image_bytes: bytes) -> Optional[Dict[str, Any]]:
    """
    Safely analyze face attributes from image bytes.

    Returns None if AI unavailable or analysis fails.

    Args:
        image_bytes: JPEG/PNG bytes of face image.

    Returns:
        Dict with attributes like age, gender, emotion, or None on failure.
    """
    # Get AI module
    ai = ai_loader.get_ai()
    if ai is None:
        return None
    try:
        # Call AI attribute analysis
        return ai.analyze_attributes(image_bytes)
    except Exception:
        # Return None on error
        return None
