# app/database/redis_client.py
import os
import sys
import redis
SRC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.insert(0, SRC_DIR)
    
from backend.config.config import Settings
import logging

logger = logging.getLogger(__name__)
settings = Settings()
# Redis connection pool
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # Return strings instead of bytes
)

def test_redis_connection():
    """Test Redis connection on startup"""
    print("REDIS_HOST:", settings.REDIS_HOST)
    print("REDIS_PORT:", settings.REDIS_PORT)
    print("REDIS_DB:", settings.REDIS_DB)
    try:
        redis_client.ping()
        logger.info("✅ Redis connection successful")
        return True
    except redis.ConnectionError:
        logger.error("❌ Redis connection failed")
        return False
    
test_redis_connection()