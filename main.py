from fastapi import FastAPI, Depends, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Item as ItemModel
from schemas import Item, ItemResponse


import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# To run locally:
# uvicorn main:app --host 0.0.0.0 --port 80 --reload
# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.getenv('DB_URL'))


@app.get("/")
async def root():
    return {"Message": "Hello World"}


@app.post('/sell/item/', response_model=ItemResponse)
async def add_item(item: Item, db: Session = Depends(get_db)):
    item_dict = item.dict()
    item_dict['price'] = int(float(item_dict['price']) * 100)
    new_item = ItemModel(**item_dict)
    db.add(new_item)
    db.commit()
    db.query()
    db.refresh(new_item)
    print(new_item.__dict__)
    return new_item

@app.delete('/unsell/item/')
async def remove_item(id: dict, db: Session = Depends(get_db)):
    id = id["id"]
    print(id)
    query = db.query(ItemModel).filter(ItemModel.id == str(id))
    original_post = query.first()
    print(original_post)
    if original_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=200)
@app.get('/all_posts/')
async def add_post(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()