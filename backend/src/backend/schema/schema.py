from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    username_or_email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str