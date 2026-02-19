from sqlmodel import Field, SQLModel, create_engine


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