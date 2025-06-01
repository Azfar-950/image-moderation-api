from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from datetime import datetime, timedelta
from config.database import tokens_collection
from schemas.token import TokenCreate, TokenResponse
from middleware.auth_middleware import verify_token, verify_admin
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
router = APIRouter()

@router.post("/tokens", response_model=TokenResponse)
async def create_token(token_data: TokenCreate, admin: dict = Depends(verify_admin)):
    token = jwt.encode({"exp": datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, algorithm="HS256")
    token_doc = {
        "token": token,
        "isAdmin": token_data.isAdmin,
        "createdAt": datetime.utcnow()
    }
    tokens_collection.insert_one(token_doc)
    return TokenResponse(**token_doc)

@router.get("/tokens")
async def list_tokens(admin: dict = Depends(verify_admin)):
    tokens = list(tokens_collection.find({}, {"_id": 0}))
    return tokens

@router.delete("/tokens/{token}")
async def delete_token(token: str, admin: dict = Depends(verify_admin)):
    result = tokens_collection.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"message": "Token deleted"}