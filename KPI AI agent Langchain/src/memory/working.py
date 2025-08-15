"""Short-term working memory"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class WorkingMemoryItem:
    """Item in working memory"""
    key: str
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Optional[timedelta] = None  # Time to live
    
    def is_expired(self) -> bool:
        """Check if item has expired"""
        if self.ttl is None:
            return False
        return datetime.now() > (self.timestamp + self.ttl)

class KPIWorkingMemory:
    """Short-term working memory for current analysis session"""
    
    def __init__(self):
        self.memory_items: Dict[str, WorkingMemoryItem] = {}
        self.access_history: List[str] = []  # LRU tracking
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """Set item in working memory"""
        ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else None
        item = WorkingMemoryItem(key=key, value=value, ttl=ttl)
        self.memory_items[key] = item
        self._update_access_history(key)
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from working memory"""
        if key not in self.memory_items:
            return None
        
        item = self.memory_items[key]
        if item.is_expired():
            del self.memory_items[key]
            return None
        
        self._update_access_history(key)
        return item.value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all non-expired items"""
        expired_keys = [k for k, v in self.memory_items.items() if v.is_expired()]
        for key in expired_keys:
            del self.memory_items[key]
        
        return {k: v.value for k, v in self.memory_items.items()}
    
    def clear(self):
        """Clear working memory"""
        self.memory_items.clear()
        self.access_history.clear()
    
    def cleanup_expired(self):
        """Remove expired items"""
        expired_keys = [k for k, v in self.memory_items.items() if v.is_expired()]
        for key in expired_keys:
            del self.memory_items[key]
    
    def _update_access_history(self, key: str):
        """Update access history for LRU tracking"""
        if key in self.access_history:
            self.access_history.remove(key)
        self.access_history.append(key)
    
    def get_recent_keys(self, limit: int = 5) -> List[str]:
        """Get recently accessed keys"""
        return self.access_history[-limit:] if len(self.access_history) > limit else self.access_history