from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AnalysisHistoryCreate(BaseModel):
    user_id: UUID
    input_text: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
