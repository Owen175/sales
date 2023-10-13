from pydantic import BaseModel


class Item(BaseModel):
    title: str
    content: str
    seller: str
    price: float
    keywords: list

    class Config:
        orm_mode = True


class SearchQuery(BaseModel):
    num_returned: int
    search: str

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: int


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True
