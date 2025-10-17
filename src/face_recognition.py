"""
Face recognition utilities for The Machine.

This module handles face detection, embedding generation, matching, and
persistent storage of face data. It integrates with external AI for advanced
features while providing fallbacks.

Key Features:
- Face ID generation from image bytes.
- Embedding storage and matching.
- Attribute analysis and metadata storage.
- Pending image processing.
- Secure encrypted storage for sensitive data.

Dependencies:
- OpenCV for image processing.
- External AI for embeddings and analysis.
- Secure storage for encrypted persistence.

Usage:
- Call recognize_faces() from video processing loops.
- Use process_pending() to batch process uploaded images.
- Data stored in facebase/ directory.
"""
import cv2
import hashlib
import json
import os
from typing import Tuple

from src import ai_loader
from src.secure_storage import encrypt_data, decrypt_data

# File paths for persistent storage
FACE_DATA_FILE = "facebase/face_data.enc"  # Encrypted face metadata
EMBEDDINGS_FILE = "facebase/face_embeddings.json"  # Face embeddings (not encrypted for performance)


def _ensure_dirs():
    """Ensure facebase directory exists for data storage."""
    if not os.path.exists("facebase"):
        os.makedirs("facebase")


def generate_face_id(face_img_bytes: bytes) -> str:
    """
    Generate a unique 8-character ID from face image bytes.

    Uses MD5 hash truncated to 8 chars for brevity.

    Args:
        face_img_bytes: Raw image bytes of the face.

    Returns:
        String ID for the face.
    """
    return hashlib.md5(face_img_bytes).hexdigest()[:8]


def load_face_data() -> dict:
    """
    Load encrypted face metadata from storage.

    Returns empty dict if file missing or decryption fails.

    Returns:
        Dict of face_id -> metadata.
    """
    _ensure_dirs()
    if os.path.exists(FACE_DATA_FILE):
        try:
            decrypted_data = decrypt_data(FACE_DATA_FILE)
            return json.loads(decrypted_data)
        except Exception:
            return {}
    return {}


def save_face_data(face_data: dict):
    """
    Save face metadata to encrypted storage.

    Args:
        face_data: Dict of face_id -> metadata to save.
    """
    encrypted_data = json.dumps(face_data)
    encrypt_data(encrypted_data, FACE_DATA_FILE)


def load_embeddings() -> dict:
    """
    Load face embeddings from JSON file.

    Returns empty dict if file missing or load fails.

    Returns:
        Dict of face_id -> embedding list.
    """
    _ensure_dirs()
    if os.path.exists(EMBEDDINGS_FILE):
        try:
            with open(EMBEDDINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_embeddings(e: dict):
    """
    Save face embeddings to JSON file.

    Args:
        e: Dict of face_id -> embedding to save.
    """
    _ensure_dirs()
    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump(e, f)


def _get_embedding_from_bytes(b: bytes):
    ai = ai_loader.get_ai()
    if ai is None:
        # Do not simulate or fabricate embeddings when AI is not present.
        # Caller should instead place the raw bytes into the pending queue
        # for the external AI to process via `process_pending()`.
        raise RuntimeError("AI implementation not found; cannot generate embedding")
    if hasattr(ai, "generate_embedding"):
        return ai.generate_embedding(b)
    raise RuntimeError("AI implementation does not implement generate_embedding")


def recognize_faces(frame, face_region: Tuple[int, int, int, int], source: str):
    x, y, w, h = face_region
    face_img = frame[y:y+h, x:x+w]
    face_bytes = cv2.imencode('.jpg', face_img)[1].tobytes()
    face_id = generate_face_id(face_bytes)

    ai = ai_loader.get_ai()

    if ai is None:
        # Don't fabricate any AI outputs. Save raw face bytes for the
        # external AI to process later. Mark the face as 'Pending'.
        pending_dir = "facebase/pending"
        if not os.path.exists(pending_dir):
            os.makedirs(pending_dir)
        pending_path = os.path.join(pending_dir, f"{face_id}.jpg")
        with open(pending_path, "wb") as f:
            f.write(face_bytes)

        # persist metadata with Pending status
        face_data = load_face_data()
        face_data[face_id] = {"attributes": None, "matched_id": None, "score": None, "status": "Pending", "source": source, "pending_path": pending_path}
        save_face_data(face_data)
        # annotate frame as pending
        cv2.putText(frame, f"ID: {face_id} (Pending)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 2)
        return "Pending"

    # If AI is present, compute embedding and match
    embeddings = load_embeddings()
    emb = _get_embedding_from_bytes(face_bytes)
    candidate_map = {k: v for k, v in embeddings.items()}
    matched_id = None
    score = 0.0
    if hasattr(ai, "match_embedding"):
        mid, score = ai.match_embedding(emb, candidate_map)
        matched_id = mid

    # draw on frame
    color = (0, 255, 0) if matched_id else (0, 0, 255)
    cv2.putText(frame, f"ID: {face_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # attribute analysis
    attributes = None
    if hasattr(ai, "analyze_attributes"):
        attributes = ai.analyze_attributes(face_bytes)
        emotion = attributes.get("dominant_emotion")
        age = attributes.get("age")
        gender = attributes.get("gender")
        cv2.putText(frame, f"Emotion: {emotion}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Age: {age}", (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Gender: {gender}", (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # persist face data and embedding
    face_data = load_face_data()
    face_data[face_id] = {"attributes": attributes, "matched_id": matched_id, "score": score, "status": "Known" if matched_id else "Unknown"}
    save_face_data(face_data)

    if matched_id is None:
        # unknown: save embedding keyed by new generated id
        embeddings[face_id] = emb
        save_embeddings(embeddings)
        return "Unknown"
    return "Known"


def register_embedding(face_id: str, embedding: list, attributes: dict = None, matched_id: str = None, score: float = None):
    """Allow an external AI to register an embedding and attributes for a face.

    This function is intended to be called by the external AI implementation
    once it has processed pending images. It updates the embeddings store
    and face metadata.
    """
    embeddings = load_embeddings()
    embeddings[face_id] = embedding
    save_embeddings(embeddings)

    face_data = load_face_data()
    entry = face_data.get(face_id, {})
    entry.update({"attributes": attributes, "matched_id": matched_id, "score": score, "status": "Known" if matched_id else "Unknown"})
    face_data[face_id] = entry
    save_face_data(face_data)


def process_pending():
    """Process pending raw face images using the external AI (if present).

    This function will scan `facebase/pending/`, run the external AI's
    `generate_embedding` and `analyze_attributes` when available, and call
    `register_embedding` to persist results.
    """
    ai = ai_loader.get_ai()
    if ai is None:
        return 0
    pending_dir = "facebase/pending"
    if not os.path.exists(pending_dir):
        return 0
    processed = 0
    for name in os.listdir(pending_dir):
        if not name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        path = os.path.join(pending_dir, name)
        with open(path, 'rb') as f:
            b = f.read()
        try:
            emb = ai.generate_embedding(b)
            attrs = ai.analyze_attributes(b) if hasattr(ai, 'analyze_attributes') else None
            fid = os.path.splitext(name)[0]
            register_embedding(fid, emb, attributes=attrs)
            os.remove(path)
            processed += 1
        except Exception:
            # don't crash on AI errors; leave file for manual processing
            continue
    return processed


def search_face_by_id(face_id, frame, face_region):
    x, y, w, h = face_region
    face_img = frame[y:y+h, x:x+w]
    face_bytes = cv2.imencode('.jpg', face_img)[1].tobytes()
    current_face_id = generate_face_id(face_bytes)
    return current_face_id == face_id