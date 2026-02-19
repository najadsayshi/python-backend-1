import os
from sqlmodel import  create_engine
from dotenv import load_dotenv
load_dotenv()  # 👈 THIS  loads the .env file ,I DIDNT KNOW THAT

DATABASE_URL = os.getenv("DATABASE_URL")
print(os.getenv("DATABASE_URL"))

engine = create_engine(DATABASE_URL,echo = True)