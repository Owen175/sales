from pydantic import BaseModel


class Item(BaseModel):
    title: str
    content: str
    seller: str
    price: float
    keywords: list

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: int
