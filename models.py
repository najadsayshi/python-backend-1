from sqlmodel import Field, SQLModel, create_engine     
from typing import Optional
class User(SQLModel, table = True):
        id : int | None = Field(default=None, primary_key=True)
        name : str
        email : str
        password : str
    

class UserCreate(SQLModel):
        name : str
        email : str
        password : str

class UserRead(SQLModel):
        id : int
        name : str
        email : str
        

class UserLogin(SQLModel):
        email : str
        password : str



class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")



class ItemCreate(SQLModel):
    title: str
    description: Optional[str] = None

class ItemUpdate(SQLModel):
       title : Optional[str] = None
       description : Optional[str] = None
