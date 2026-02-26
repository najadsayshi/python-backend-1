from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, Session, select

from db import engine
from models import User, UserCreate, UserLogin, ItemCreate, Item, ItemUpdate, UserRead
from auth import create_token, verify_token

app = FastAPI()

#middleware - CORS
from fastapi.middleware.cors import CORSMiddleware
origins = [

     '*'
 ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#for render -deployment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app.mount("/static", StaticFiles(directory="frontend"), name="static")
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# Dependency to create DB session
def create_session():
    with Session(engine) as session:
        yield session


# @app.get("/")
# async def root():
#     return {"message": "Hello world"}


@app.post("/signup", response_model=UserRead)
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

    access_token = create_token(db_user.id,db_user.name)

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
        "user_id": payload["sub"],
        "name" : payload["name"]
    }

# getting user id whenever we want using jwt token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                    db: Session = Depends(create_session)):
    
    token = credentials.credentials
    
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code = 401, detail = "Invalid or expired token")
    
    user_id = payload["sub"]

    statement = select(User).where(User.id ==user_id)

    user = db.exec(statement).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not Found")
    
    return user




@app.post("/items")
def create_item(
                    item : ItemCreate,
                    db : Session = Depends(create_session),
                    Current_user : User = Depends(get_current_user)
                ):
    
    db_item = Item(
        title = item.title,
        description = item.description,
        owner_id = Current_user.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    

@app.put("/items/{item_id}")

def update_item(
    item_id : int,
    updated_item  : ItemUpdate,
    db : Session = Depends(create_session),
    current_user : User =  Depends(get_current_user),
):
    statement = select(Item).where(Item.id ==item_id)

    db_item = db.exec(statement).first()

    if not db_item:
        raise HTTPException(status_code = 404,detail = "Item not found brother")
    

    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code = 403,detail = "Not authorized for you to do that")
    
    if updated_item.title is not None:
        db_item.title = updated_item.title

    
    if updated_item.description is None:
        db_item.description = db_item.description 
    else:
        db_item.description= updated_item.description
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item



@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(create_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Item).where(Item.id == item_id)
    db_item = db.exec(statement).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(db_item)
    db.commit()

    return {"message": "Item deleted"}


@app.get("/items")
def get_items(
    db: Session = Depends(create_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Item).where(Item.owner_id == current_user.id)
    items = db.exec(statement).all()
    return items