"""Clean admin module used as a temporary safe import target.

This provides the tri-authentication and admin menu functions. Once
`src/admin.py` is fully cleaned we can swap back imports to that file.
"""

import json
import os
import hashlib
from getpass import getpass
from pathlib import Path
from typing import Dict, Any

from src import ai_loader
from src import face_recognition
from src.secure_storage import decrypt_data, encrypt_data, generate_key


FACEBASE_DIR = Path("facebase")
PENDING_DIR = FACEBASE_DIR / "pending"
SECURE_FILE = Path("secure_data.enc")
ADMIN_FACE = Path("admin_face.jpg")


def _ensure_dirs() -> None:
    """Ensure that necessary directories exist for facebase and pending files."""
    FACEBASE_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_DIR.mkdir(parents=True, exist_ok=True)


def _hash_password(password: str) -> str:
    """Hash the password using SHA256 for secure storage."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_secure() -> Dict[str, Any]:
    """Load encrypted secure data from file, return dict or empty on failure."""
    _ensure_dirs()
    if not SECURE_FILE.exists():
        return {}
    try:
        dec = decrypt_data(str(SECURE_FILE))
        return json.loads(dec)
    except Exception:
        return {}


def save_secure(data: Dict[str, Any]) -> None:
    """Save secure data dict to encrypted file."""
    _ensure_dirs()
    encrypt_data(json.dumps(data), str(SECURE_FILE))


def ensure_key() -> None:
    try:
        generate_key()
    except Exception:
        pass


def authenticate_admin() -> bool:
    ensure_key()
    data = load_secure()
    stored = data.get("admin_password")
    if not stored:
        print("No admin password set. Creating one now.")
        while True:
            p1 = getpass("New admin password: ")
            p2 = getpass("Confirm password: ")
            if p1 != p2:
                print("Passwords do not match. Try again.")
                continue
            if len(p1) < 6:
                print("Choose a stronger password (min 6 chars).")
                continue
            data["admin_password"] = _hash_password(p1)
            save_secure(data)
            print("Admin password set.")
            return True
    for _ in range(3):
        p = getpass("Admin password: ")
        if _hash_password(p) == stored:
            return True
        print("Invalid password.")
    return False


def tri_authenticate() -> bool:
    if not authenticate_admin():
        return False
    # face and voice checks are optional and best-effort
    try:
        import cv2
        if ADMIN_FACE.exists():
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret and hasattr(ai_loader.get_ai(), "verify_face"):
                ai = ai_loader.get_ai()
                if ai is not None:
                    try:
                        live_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                        ref = cv2.imread(str(ADMIN_FACE))
                        if ref is not None:
                            ref_bytes = cv2.imencode('.jpg', ref)[1].tobytes()
                            if ai.verify_face(live_bytes, ref_bytes):
                                pass
                            else:
                                return False
                    except Exception:
                        pass
    except Exception:
        pass
    # voice fallback: typed passphrase
    data = load_secure()
    stored_phrase_hash = data.get("voice_passphrase_hash")
    if stored_phrase_hash:
        phrase = input("Enter your voice passphrase: ").strip()
        if _hash_password(phrase) != stored_phrase_hash:
            return False
    return True


def list_pending_files() -> None:
    _ensure_dirs()
    pending = list(PENDING_DIR.glob("*"))
    if not pending:
        print("No pending files found in facebase/pending/")
        return
    print(f"Pending files ({len(pending)}):")
    face_data = {}
    try:
        face_data = face_recognition.load_face_data()
    except Exception:
        pass
    for p in pending:
        fid = p.stem
        meta = face_data.get(fid, {}) if isinstance(face_data, dict) else {}
        status = meta.get("status") if isinstance(meta, dict) else None
        src = meta.get("source") if isinstance(meta, dict) else None
        print(f" - {p.name} | id={fid} status={status} source={src}")


def force_process_pending() -> int:
    _ensure_dirs()
    ai = ai_loader.get_ai()
    if ai is None:
        print("AI mode unavailable.")
        return 0
    try:
        processed = face_recognition.process_pending()
        return int(processed) if processed is not None else 0
    except Exception:
        return 0


def admin_menu() -> None:
    _ensure_dirs()
    print("--- Machine Admin Menu ---")
    if not tri_authenticate():
        print("Authentication failed. Exiting admin menu.")
        return
    while True:
        print("\nSelect an option:")
        print("1) List pending files")
        print("2) Force process pending files")
        print("3) Exit")
        choice = input("> ").strip()
        if choice == "1":
            list_pending_files()
        elif choice == "2":
            processed = force_process_pending()
            print(f"Processed {processed} pending files.")
        elif choice == "3":
            break
        else:
            print("Unknown option")
