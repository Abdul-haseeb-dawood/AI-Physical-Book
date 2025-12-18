from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import hashlib


class CacheService:
    """
    Service to cache query responses to improve performance
    """
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = timedelta(seconds=default_ttl)
    
    def _generate_key(self, query: str, context: str = "") -> str:
        """
        Generate a cache key based on query and context
        """
        key_string = f"{query}:{context}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, query: str, context: str = "") -> Optional[Dict[str, Any]]:
        """
        Get cached response if available and not expired
        """
        key = self._generate_key(query, context)
        
        if key in self.cache:
            cached_item = self.cache[key]
            
            # Check if item is expired
            if datetime.utcnow() > cached_item["expires_at"]:
                del self.cache[key]  # Remove expired item
                return None
            
            return cached_item["data"]
        
        return None
    
    def set(self, query: str, context: str = "", ttl: Optional[int] = None):
        """
        Set a response in cache
        """
        key = self._generate_key(query, context)
        
        if ttl is None:
            ttl = self.default_ttl
        else:
            ttl = timedelta(seconds=ttl)
        
        self.cache[key] = {
            "data": data,
            "expires_at": datetime.utcnow() + ttl
        }
    
    def invalidate(self, query: str, context: str = ""):
        """
        Remove a specific item from cache
        """
        key = self._generate_key(query, context)
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """
        Clear all cache
        """
        self.cache.clear()
    
    def cleanup_expired(self):
        """
        Remove all expired items from cache
        """
        expired_keys = []
        now = datetime.utcnow()
        
        for key, cached_item in self.cache.items():
            if now > cached_item["expires_at"]:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]