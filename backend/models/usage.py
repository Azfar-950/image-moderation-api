from datetime import datetime
from pydantic import BaseModel

class Usage(BaseModel):
    token: str
    endpoint: str
    timestamp: datetime