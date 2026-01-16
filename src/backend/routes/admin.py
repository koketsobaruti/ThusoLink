# # app/routers/admin.py (create this for testing)
# from fastapi import APIRouter, Depends, HTTPException, status
# from ..tasks.cleanup import cleanup_expired_tokens
# from ..auth.jwt_bearer import get_current_user
# from ..models.user import User

# router = APIRouter()

# @router.post("/cleanup-tokens")
# async def trigger_cleanup(
#     current_user: User = Depends(get_current_user)
# ):
#     """
#     Manually trigger token cleanup (for testing)
#     In production, you might want to add admin role check
#     """
#     deleted_count = cleanup_expired_tokens()
    
#     return {
#         "message": f"Cleaned up {deleted_count} expired tokens",
#         "deleted_count": deleted_count
#     }