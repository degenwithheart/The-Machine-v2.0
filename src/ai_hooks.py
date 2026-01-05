"""Event-driven AI integration"""

class AIHooks:
    def __init__(self, adapter):
        self.adapter = adapter
        self.hooks = []
    
    def register_hook(self, event_type, callback):
        """Register event hook"""
        self.hooks.append({'type': event_type, 'callback': callback})
    
    def trigger(self, event_type, data):
        """Trigger hooks for event"""
        for hook in self.hooks:
            if hook['type'] == event_type:
                try:
                    hook['callback'](data)
                except Exception as e:
                    print(f"Hook error: {e}")
