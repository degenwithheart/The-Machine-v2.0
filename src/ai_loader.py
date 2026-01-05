"""Dynamic AI module loading"""
import importlib.util
import os

class AILoader:
    @staticmethod
    def load_module(module_path):
        """Dynamically load AI module"""
        try:
            spec = importlib.util.spec_from_file_location("ai_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Failed to load module: {e}")
            return None
