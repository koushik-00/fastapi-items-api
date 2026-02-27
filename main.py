from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine, get_db
from fastapi import Depends
import models
import auth

models.Base.metadata.create_all(bind=engine)

class Addition(BaseModel):
    num1: int
    num2: int

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemSchema(ItemCreate):
    id: int
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

apb = FastAPI()

@apb.get('/')
def ff():
    return {'message' : 'Hello world'}

# @apb.get('/items/{item_id}')
# async def rI(item_id: int):
#     return {"items_id": item_id}

@apb.post('/add')
async def add(item: Addition):
    return {"sum": item.num1 + item.num2}

# -- GET --

@apb.get('/items')
def get_items(db: Session = Depends(get_db)):
    return db.execute(select(models.Item)).scalars().all()

@apb.get('/items/{item_id}')
def get_item(item_id: int, db: Session = Depends(get_db)):
    stmt = db.get(models.Item, item_id)
    if not stmt:
        raise HTTPException(status_code = 404, detail = "Item not found")
    return stmt

# -- POST --
# create a models.Item object, add it to the db, commit it
@apb.post('/items', response_model=ItemSchema)
def create_item(itm: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name = itm.name, price = itm.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# -- PUT --
@apb.put('/items/{item_id}', response_model=ItemSchema)
def put_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.get(models.Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    a = item.model_dump()
    for key, value in a.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item
    

# -- DELETE --
@apb.delete('/items/{item_id}')
def delete_item(item_id: int, db: Session = Depends(get_db)):
    del_item = db.get(models.Item, item_id)
    if not del_item:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(del_item)
    db.commit()
    return {'message': 'Item deleted successfully'}


@apb.post('/register')
async def user_register(new_user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.execute(select(models.User).filter(models.User.username == new_user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail = "Username already exists")
    user = models.User(username=new_user.username, hashed_password = auth.hash_password(new_user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


    