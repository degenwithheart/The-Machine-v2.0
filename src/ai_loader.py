"""
Dynamic AI loader.

This module attempts to load an external AI implementation dropped in the
project root `ai/` directory (preferred). If none is present it will load
the internal `src.ai_core` module as a fallback. The external AI must expose
the same functions as `src.ai_core` (for example `generate_embedding`,
`match_embedding`, `analyze_attributes`, `predict_violent_event`,
`classify_relevance`, `ingest_stream`).

To provide your AI implementation, create a package at `./ai` with an
`__init__.py` or `impl.py` exposing the required functions. Example:

ai/
  __init__.py   # should expose functions or import from impl
  impl.py

The loader loads the external module by filepath which avoids installing it.

Purpose:
- Enable drop-in AI implementations without code changes.
- Support multiple AI backends via file-based loading.
- Avoid import-time dependencies on heavy AI libraries.
- Provide clear failure modes when AI is missing.

Loading Strategy:
1. Check for ai/ directory in repo root.
2. Try package import (ai/__init__.py).
3. Fallback to ai/impl.py if package fails.
4. Return None if no AI found.

Security Notes:
- Loads from local filesystem only.
- No network or remote code execution.
- AI code runs with same permissions as main process.
"""
import importlib
import importlib.util
import os
import sys
from types import ModuleType


# Determine repository root for relative path loading
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_module_from_path(name: str, path: str) -> ModuleType:
    """
    Load a Python module from a file path using importlib.

    This allows loading AI implementations without installing them.

    Args:
        name: Module name for sys.modules.
        path: Absolute path to the Python file.

    Returns:
        Loaded module object.

    Raises:
        ImportError: If file cannot be loaded or executed.
    """
    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise ImportError(f"Cannot load module from {path}")
    # Create module from spec
    mod = importlib.util.module_from_spec(spec)
    # Get the loader and execute the module
    loader = spec.loader
    assert loader is not None
    loader.exec_module(mod)
    return mod


def get_ai():
    """
    Return the external AI module if present, otherwise return None.

    The caller should treat a None return value as "AI not installed yet" and
    avoid producing AI-derived outputs. This loader intentionally does NOT
    fall back to a simulated implementation.

    Returns:
        AI module object or None.

    Notes:
        - Checks for ai/ directory first.
        - Tries package import, then impl.py.
        - Returns None on any loading failure.
        - Thread-safe as it only reads filesystem.
    """
    # Check if ai/ directory exists in repo root
    if os.path.isdir(os.path.join(REPO_ROOT, "ai")):
        # Temporarily add repo root to sys.path for import
        if REPO_ROOT not in sys.path:
            sys.path.insert(0, REPO_ROOT)
        try:
            # Try importing as package
            return importlib.import_module("ai")
        except Exception:
            # Fallback to impl.py file
            impl_path = os.path.join(REPO_ROOT, "ai", "impl.py")
            if os.path.exists(impl_path):
                try:
                    return _load_module_from_path("ai_impl", impl_path)
                except Exception:
                    return None
    # Return None if no AI found
    return None
