"""Redis caching service."""

from typing import Any, Optional
from loguru import logger
import json
import pickle


class RedisCache:
    """Redis caching service."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize Redis cache.
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self.client = None
        self._connect()

    def _connect(self):
        """Connect to Redis."""
        try:
            import redis
            self.client = redis.from_url(self.redis_url)
            self.client.ping()
            logger.info(f"Connected to Redis: {self.redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None

    def set(
        self,
        key: str,
        value: Any,
        expiration_seconds: Optional[int] = 3600,
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            expiration_seconds: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.warning("Redis client not available")
            return False

        try:
            # Serialize value
            if isinstance(value, str):
                serialized = value
            else:
                serialized = pickle.dumps(value)

            self.client.set(key, serialized, ex=expiration_seconds)
            logger.debug(f"Cache set: {key}")
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self.client:
            logger.warning("Redis client not available")
            return None

        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                # Try to deserialize
                try:
                    return pickle.loads(value)
                except:
                    return value
            logger.debug(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting cache: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            self.client.delete(key)
            logger.debug(f"Cache deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False

    def clear(self) -> bool:
        """
        Clear entire cache.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            self.client.flushdb()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if exists, False otherwise
        """
        if not self.client:
            return False

        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache existence: {e}")
            return False

    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment counter in cache.
        
        Args:
            key: Cache key
            amount: Amount to increment
            
        Returns:
            New value or None if error
        """
        if not self.client:
            return None

        try:
            result = self.client.incrby(key, amount)
            return result
        except Exception as e:
            logger.error(f"Error incrementing cache: {e}")
            return None

    def decrement(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Decrement counter in cache.
        
        Args:
            key: Cache key
            amount: Amount to decrement
            
        Returns:
            New value or None if error
        """
        if not self.client:
            return None

        try:
            result = self.client.decrby(key, amount)
            return result
        except Exception as e:
            logger.error(f"Error decrementing cache: {e}")
            return None

    def get_all_keys(self, pattern: str = "*") -> list:
        """
        Get all keys matching pattern.
        
        Args:
            pattern: Key pattern (e.g., "user:*")
            
        Returns:
            List of keys
        """
        if not self.client:
            return []

        try:
            keys = self.client.keys(pattern)
            return [k.decode() if isinstance(k, bytes) else k for k in keys]
        except Exception as e:
            logger.error(f"Error getting keys: {e}")
            return []
