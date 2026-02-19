import os
from sqlmodel import  create_engine

DATABASE_URL = OS.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL,echo = True)
engine = create_engine("postgresql://neondb_owner:npg_0IVehsEQPKq5@ep-holy-moon-abtgvn02-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require",echo=True)




