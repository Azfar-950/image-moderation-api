from datetime import datetime
from pydantic import BaseModel

class Token(BaseModel):
    token: str
    isAdmin: bool
    createdAt: datetime
    expiresAt: datetime | None = None