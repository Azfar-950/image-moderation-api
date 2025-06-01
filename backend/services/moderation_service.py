from fastapi import UploadFile
import random

async def moderate_image(file: UploadFile):
    # Mock moderation logic (replace with real ML model in production)
    categories = ["violence", "nudity", "hate_symbols", "self_harm", "extremist"]
    return {
        "is_safe": random.choice([True, False]),
        "categories": [
            {"category": cat, "confidence": round(random.uniform(0, 1), 2)}
            for cat in categories
        ]
    }