"""Admin utilities for The Machine (canonical module).

This file provides a small admin interface used by main.py. It is kept
intentionally minimal and avoids optional heavy imports at module
load time.
"""

import json
import hashlib
from getpass import getpass
from pathlib import Path
from typing import Dict, Any
import time
import os

from src import ai_loader
from src import face_recognition
from src.secure_storage import decrypt_data, encrypt_data, generate_key


FACEBASE_DIR = Path("facebase")
PENDING_DIR = FACEBASE_DIR / "pending"
SECURE_FILE = Path("secure_data.enc")
ADMIN_FACE = Path("admin_face.jpg")
LOGS_DIR = Path("logs")
SURVEILLANCE_LOG = LOGS_DIR / "surveillance.log"
EVENT_LOG = LOGS_DIR / "events.log"


def cross_platform_timeout(func, timeout: float):
    """Run func with timeout, cross-platform.
    
    Uses signal on Unix-like systems, threading on Windows.
    Raises TimeoutError if func doesn't complete within timeout seconds.
    """
    import signal
    if os.name == 'nt':  # Windows
        # Windows doesn't support signal.SIGALRM, use threading
        import threading
        result = [None]
        exception = [None]
        def target():
            try:
                result[0] = func()
            except Exception as e:
                exception[0] = e
        t = threading.Thread(target=target)
        t.start()
        t.join(timeout)
        if t.is_alive():
            raise TimeoutError("Function timed out")
        if exception[0]:
            raise exception[0]
        return result[0]
    else:  # Unix-like
        def handler(signum, frame):
            raise TimeoutError("Function timed out")
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(timeout))
        try:
            return func()
        finally:
            signal.alarm(0)


def _ensure_dirs() -> None:
    FACEBASE_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_secure() -> Dict[str, Any]:
    _ensure_dirs()
    if not SECURE_FILE.exists():
        return {}
    try:
        dec = decrypt_data(str(SECURE_FILE))
        return json.loads(dec)
    except Exception:
        return {}


def save_secure(data: Dict[str, Any]) -> None:
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
    """Perform minimal tri-auth: password (required), optional face/voice."""
    if not authenticate_admin():
        return False

    # Optional face check (best-effort)
    try:
        import cv2  # optional dependency

        if ADMIN_FACE.exists():
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                ai = ai_loader.get_ai()
                if ai is not None and hasattr(ai, "verify_face"):
                    try:
                        live = cv2.imencode('.jpg', frame)[1].tobytes()
                        ref = cv2.imread(str(ADMIN_FACE))
                        if ref is not None:
                            refb = cv2.imencode('.jpg', ref)[1].tobytes()
                            if not ai.verify_face(live, refb):
                                return False
                    except Exception:
                        pass
    except Exception:
        # OpenCV not installed or camera unavailable
        pass

    # Optional voice fallback: typed passphrase
    data = load_secure()
    stored_phrase_hash = data.get("voice_passphrase_hash")
    if stored_phrase_hash:
        phrase = input("Enter your voice passphrase: ").strip()
        if _hash_password(phrase) != stored_phrase_hash:
            return False
    return True


def list_pending_files() -> None:
    """List files in facebase/pending with any known metadata."""
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


def log_event(message: str, log_file: Path = EVENT_LOG, level: str = "INFO") -> None:
    """Log an event with level, and analyze text if AI available."""
    _ensure_dirs()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ai = ai_loader.get_ai()
    analysis = ""
    if ai and hasattr(ai, "analyze_sentiment"):
        try:
            sentiment = ai.analyze_sentiment(message)
            analysis += f" Sentiment: {sentiment}"
        except Exception:
            pass
    if ai and hasattr(ai, "detect_threat"):
        try:
            threat = ai.detect_threat(message)
            if threat.get("threat_level") != "low":
                analysis += f" Threat: {threat}"
        except Exception:
            pass
    if ai and hasattr(ai, "detect_sarcasm"):
        try:
            sarcasm = ai.detect_sarcasm(message)
            if sarcasm > 0.5:
                analysis += f" Sarcasm: {sarcasm:.2f}"
        except Exception:
            pass
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] [{level}] {message}{analysis}\n")


def view_logs(log_file: Path = EVENT_LOG) -> None:
    """View the contents of the event log."""
    _ensure_dirs()
    if not log_file.exists():
        print("No logs found.")
        return
    with open(log_file, "r") as f:
        content = f.read()
    print("--- Event Logs ---")
    print(content or "No events logged.")


def system_status() -> None:
    """Display system status: pending files, AI status, surveillance mode, resources."""
    _ensure_dirs()
    pending_count = len(list(PENDING_DIR.glob("*")))
    ai = ai_loader.get_ai()
    ai_status = "Loaded" if ai else "Not loaded"
    surveillance_active = load_secure().get("surveillance_active", False)
    monitor = self_monitor()
    print("--- System Status ---")
    print(f"Pending files: {pending_count}")
    print(f"AI status: {ai_status}")
    print(f"Surveillance active: {surveillance_active}")
    print(f"CPU: {monitor.get('cpu_percent', 'N/A')}%")
    print(f"Memory: {monitor.get('memory_percent', 'N/A')}%")
    print(f"Performance: {monitor.get('performance_score', 'N/A')}")


def configure_alerts() -> None:
    """Configure alert settings (placeholder for now)."""
    print("Alert configuration not implemented yet. (Would set email/SMS alerts)")


def start_surveillance() -> None:
    """Start surveillance mode."""
    data = load_secure()
    data["surveillance_active"] = True
    save_secure(data)
    log_event("Surveillance started")
    print("Surveillance mode activated.")


def stop_surveillance() -> None:
    """Stop surveillance mode."""
    data = load_secure()
    data["surveillance_active"] = False
    save_secure(data)
    log_event("Surveillance stopped")
    print("Surveillance mode deactivated.")


def self_monitor() -> Dict[str, Any]:
    """Monitor system resources and AI performance."""
    try:
        import psutil  # optional
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        perf = 1.0 - (cpu + memory) / 200.0
    except ImportError:
        cpu = memory = perf = "unknown"
    ai_metrics = {}
    ai = ai_loader.get_ai()
    if ai and hasattr(ai, "self_monitor"):
        try:
            ai_metrics = ai.self_monitor()
        except Exception:
            ai_metrics = {"ai_status": "error"}
    return {"cpu_percent": cpu, "memory_percent": memory, "performance_score": perf, **ai_metrics}


def adaptive_learn(feedback: Dict[str, Any]) -> None:
    """Adjust behavior based on feedback."""
    data = load_secure()
    if "threshold" not in data:
        data["threshold"] = 0.8
    if feedback.get("action") == "lower_threshold":
        data["threshold"] = max(0.5, data["threshold"] - 0.1)
        log_event("Lowered threshold due to feedback", level="INFO")
    elif feedback.get("action") == "raise_threshold":
        data["threshold"] = min(0.95, data["threshold"] + 0.1)
        log_event("Raised threshold due to feedback", level="INFO")
    save_secure(data)


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
        print("3) View event logs")
        print("4) System status")
        print("5) Start surveillance")
        print("6) Stop surveillance")
        print("7) Configure alerts")
        print("8) Exit")
        choice = input("> ").strip()
        if choice == "1":
            list_pending_files()
        elif choice == "2":
            processed = force_process_pending()
            print(f"Processed {processed} pending files.")
        elif choice == "3":
            view_logs()
        elif choice == "4":
            system_status()
        elif choice == "5":
            start_surveillance()
        elif choice == "6":
            stop_surveillance()
        elif choice == "7":
            configure_alerts()
        elif choice == "8":
            break
        else:
            print("Unknown option")


if __name__ == "__main__":
    admin_menu()
