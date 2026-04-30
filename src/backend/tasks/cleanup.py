# app/tasks/cleanup.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..database.connection import SessionLocal
from ..models.auth.token_blacklist import TokenBlacklist
import logging

logger = logging.getLogger(__name__)

def cleanup_expired_tokens():
    """
    Remove expired tokens from blacklist.
    This runs as a background task.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        
        # Delete expired tokens
        deleted_count = db.query(TokenBlacklist).filter(
            TokenBlacklist.expires_at < now
        ).delete()
        
        db.commit()
        logger.info(f"✅ Cleaned up {deleted_count} expired blacklisted tokens")
        
        return deleted_count
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Cleanup error: {str(e)}")
        return 0
    finally:
        db.close()