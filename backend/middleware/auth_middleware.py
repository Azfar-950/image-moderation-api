from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config.database import tokens_collection
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        token_doc = tokens_collection.find_one({"token": token})
        if not token_doc:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {"token": token, "isAdmin": token_doc["isAdmin"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_admin(token_data: dict = Depends(verify_token)):
    if not token_data["isAdmin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return token_data