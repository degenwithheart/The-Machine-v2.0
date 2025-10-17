"""
AI hook utilities.

Provides a thin wrapper around optional AI stream ingestion functions. The
functions call into the external AI when present and return its response or
None when no AI is installed.

Purpose:
- Hook into AI for event processing without tight coupling.
- Enable optional AI features in surveillance pipelines.
- Provide fallback behavior when AI is unavailable.
- Centralize event ingestion logic.

Usage:
- Call ingest_event() from surveillance loops.
- Expect None when AI not loaded, dict when processed.
- Handles exceptions gracefully to avoid breaking streams.
"""
from typing import Any, Dict, Optional
from src import ai_loader


def ingest_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process a surveillance event using external AI if available.

    Attempts full ingestion first, falls back to partial analysis.
    Returns None if AI unavailable or processing fails.

    Args:
        event: Dict containing event data from surveillance streams.

    Returns:
        Dict with AI analysis results, or None.
        Example: {'score': 0.8, 'relevance': 'relevant', 'attributes': {...}}

    Notes:
        - Full ingestion includes storage to file.
        - Partial fallback uses prediction and classification only.
        - Thread-safe as it doesn't modify shared state.
    """
    # Retrieve the AI module (None if not loaded)
    ai = ai_loader.get_ai()
    if ai is None:
        return None
    try:
        # Try full stream ingestion if available
        if hasattr(ai, 'ingest_stream'):
            return ai.ingest_stream(event)
        # Fallback: partial analysis using available functions
        out = {'score': None, 'relevance': None}
        # Add violent event prediction if available
        if hasattr(ai, 'predict_violent_event'):
            out['score'] = ai.predict_violent_event(event)
        # Add relevance classification if available
        if hasattr(ai, 'classify_relevance'):
            out['relevance'] = ai.classify_relevance(event)
        # Return partial results
        return out
    except Exception:
        # Return None on any error to prevent stream interruption
        return None
