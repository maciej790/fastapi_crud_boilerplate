from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Union

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(index=True)
    
class UserIn(BaseModel):
    username: str = Field(index=True)
    password: str = Field(index=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Union[str, None] = None
