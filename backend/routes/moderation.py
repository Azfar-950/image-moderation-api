from fastapi import APIRouter, UploadFile, File, Depends
from config.database import usages_collection
from datetime import datetime
from middleware.auth_middleware import verify_token
from services.moderation_service import moderate_image

router = APIRouter()

@router.post("/moderate")
async def moderate(file: UploadFile = File(...), token_data: dict = Depends(verify_token)):
    # Log usage
    usage = {
        "token": token_data["token"],
        "endpoint": "/moderate",
        "timestamp": datetime.utcnow()
    }
    usages_collection.insert_one(usage)
    
    # Analyze image
    result = await moderate_image(file)
    return result