from fastapi import FastAPI, Depends, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Item as ItemModel
from schemas import Item, ItemResponse, SearchQuery

import os
from dotenv import load_dotenv

from search import search_function_ranker

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

@app.get('/search/')
async def search(search_query: SearchQuery, db: Session = Depends(get_db)):
    search_query = search_query.dict()
    query_statement = search_query["search"]
    num_returned = search_query["num_returned"]
    all_items = db.query(ItemModel).order_by(ItemModel.id.asc()).all()
    keyword_list = []
    for item in all_items:
        keyword_list.append(item.keywords)
    sfr = search_function_ranker.search(query_statement, keyword_list)
    if len(sfr) < num_returned:
        num = len(sfr)
    else:
        num = num_returned
    sfr_sorted = sorted(sfr, reverse=True)
    return_items = []
    for i in range(num):
        id = sfr.index(sfr_sorted[i])
        return_items.append(all_items[id])

    return return_items