from jose import jwt 
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(user_id):

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub" : str(user_id),
        "exp" : expire
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    return token
    

def verify_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY , ALGORITHM)
        return payload
    except (JWTerror):
        return NOne
