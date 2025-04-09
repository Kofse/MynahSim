import json
from datetime import datetime, timedelta
from pathlib import Path

class Memory:
    def __init__(self):
        self.file = Path("memory.json")
        if not self.file.exists():
            self.file.write_text("{}")
        self.data = json.loads(self.file.read_text())
    
    def remember(self, key: str, value: str, ttl_days: int = 30):
        self.data[key] = {
            "value": value,
            "expiry": (datetime.now() + timedelta(days=ttl_days)).isoformat()
        }
        self._save()
    
    def recall(self, key: str) -> str:
        entry = self.data.get(key)
        if entry and datetime.fromisoformat(entry["expiry"]) > datetime.now():
            return entry["value"]
        return None
    
    def _save(self):
        self.file.write_text(json.dumps(self.data, indent=2))
