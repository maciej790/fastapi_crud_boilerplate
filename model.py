from pydantic import BaseModel
from sqlmodel import Field, SQLModel

#db table model
class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    
#for update
class UpdateTaskModel(BaseModel):
    title : str
    description : str   

#for create
class CreateTask(BaseModel):
    title : str
    description : str  
    