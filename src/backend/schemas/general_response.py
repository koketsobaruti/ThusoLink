from typing import Optional
from pydantic import BaseModel

class GeneralResponse(BaseModel):
    status: int
    message: Optional[str] = None
    data: Optional[dict] = None