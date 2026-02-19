from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select
from db import engine
from models import User,UserCreate,UserLogin
from auth import create_token
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
        email = user.email.lower().strip()
        statement = select(User).where(User.email==email)
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

        email = user.email.lower().strip()
        statement = select (User).where(User.email == email)
        db_user = session.exec(statement).first()
        print(user.password)
        if not db_user or user.password != db_user.password:
            raise HTTPException(status_code = 400, detail = "Invalid credentials Mommy")
        
        access_token = create_token(db_user.id)
        return {"Acess token ": access_token,
                "status " :"Good shit baby" }

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import verify_token

security = HTTPBearer()

@app.get("/profile")
def profile(credentials : HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"Message": "YOU ARE LOGGED IN !","user_id" : payload["sub"] }