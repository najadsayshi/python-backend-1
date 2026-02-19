from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select
from db import engine
from models import User,UserCreate,UserLogin

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)  


@app.get("/")
async def root():
    return {"message":"Hello world"}


@app.post("/signup")
def signup(user: UserCreate):

    with Session(engine) as session:
        statement = select(User).where(User.email==user.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(status_code = 400, detail = "User already available mommy")
        db_user = User(
            name = user.name,
            email = user.email,
            password = user.password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.post("/login")
def login(user: UserLogin ):

    with Session(engine) as session:

        statement = select (User).where(User.email == user.email)
        db_user = session.exec(statement).first()
        print(user.password)
        if not db_user or user.password != db_user.password:
            raise HTTPException(status_code = 400, detail = "Invalid credentials Mommy")
        
        return {"Message" : "Login Successfull Mommy"}

