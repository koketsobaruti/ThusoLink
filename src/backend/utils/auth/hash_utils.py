from passlib.context import CryptContext
import bcrypt
# import logger from logger_utils
from ..logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Hash Utils")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return the bcrypt hash of the password."""
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pass.decode("utf-8")  # ✅ convert bytes → string for DB

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        # If the hash is hex-encoded (old data), decode it first
        if hashed_password.startswith("\\x"):
            import binascii
            hashed_password = binascii.unhexlify(hashed_password[2:]).decode("utf-8")

        # bcrypt.checkpw handles the comparison including the salt
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False
