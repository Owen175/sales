import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import get_db
from models import User

load_dotenv('.env')
KEY = os.getenv('KEY')
EXPIRATION = int(os.getenv('EXPIRATION'))
ALGORITHM = int(os.getenv('ALGORITHM'))


def get_token(data: dict):
    d = data.copy().update({"exp", datetime.utcnow() + timedelta(minutes=EXPIRATION)})
    return jwt.encode(d, KEY, algorithm=ALGORITHM)

def get_user(token: str, db: Session = Depends(get_db)):
    exception = HTTPException(401)
    try:
        pl = jwt.decode(token, key=KEY, algorithms=[ALGORITHM])
        uid = pl.get("uid")
        if uid is None:
            raise exception
    except JWTError:
        raise exception

    return db.query(User).filter(User.uid == uid).first()
