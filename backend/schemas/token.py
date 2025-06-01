from pydantic import BaseModel

class TokenCreate(BaseModel):
    isAdmin: bool

class TokenResponse(BaseModel):
    token: str
    isAdmin: bool
    createdAt: str