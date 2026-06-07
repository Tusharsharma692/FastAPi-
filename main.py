from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name:str
    age:int
    roll_No:int


app=FastAPI()
# POST API and DATA validation


@app.post("/items")
def create_item(id:str,price:int):
    return {
        "Message":"Item created successfully",
        "id":id,
        "price":price
    }


@app.post("/users")
def create_user(dic:dict):
    return {
        "Message":"User created successfully",
        "data":dic
    }


# using pydantic model for data validation

@app.post("/USERS")
def create_user(user:User):
    return {
        "Message":"User created successfully",
        "data":user
    }