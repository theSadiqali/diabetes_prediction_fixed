from typing import Optional
from sqlmodel import SQLModel, Field
import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    probability: float
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
