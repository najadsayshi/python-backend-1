from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, Session, select

from db import engine
from models import User, UserCreate, UserLogin
from auth import create_token, verify_token

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# Dependency to create DB session
def create_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(create_session)):

    email = user.email.lower().strip()

    statement = select(User).where(User.email == email)
    existing_user = db.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(
        name=user.name,
        email=email,
        password=user.password  # (hash this if using hashing)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(create_session)):

    email = user.email.lower().strip()

    statement = select(User).where(User.email == email)
    db_user = db.exec(statement).first()

    if not db_user or user.password != db_user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_token(db_user.id)

    return {
        "access_token": access_token
    }


security = HTTPBearer()


@app.get("/profile")
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        "message": "YOU ARE LOGGED IN!",
        "user_id": payload["sub"]
    }
