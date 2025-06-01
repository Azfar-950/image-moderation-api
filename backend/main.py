from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, moderation
from jose import jwt
from datetime import datetime, timedelta
from config.database import tokens_collection
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI(title="Image Moderation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create default admin token if no tokens exist
@app.on_event("startup")
async def create_default_admin_token():
    if tokens_collection.count_documents({}) == 0:
        token = jwt.encode({"exp": datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, algorithm="HS256")
        token_doc = {
            "token": token,
            "isAdmin": True,
            "createdAt": datetime.utcnow()
        }
        tokens_collection.insert_one(token_doc)
        print(f"Default admin token created: {token}")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(moderation.router, tags=["moderation"])

@app.get("/")
def read_root():
    return {"message": "Image Moderation API"}