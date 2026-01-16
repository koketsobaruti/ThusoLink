# app/models/token_blacklist.py
from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from ...database.connection import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    
    jti = Column(String(36), primary_key=True)  # JWT ID (UUID)
    user_id = Column(String, nullable=False)  # Track which user's token
    token_type = Column(String(10), nullable=False)  # "access" or "refresh"
    blacklisted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)  # When token naturally expires