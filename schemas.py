from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True