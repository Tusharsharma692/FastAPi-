from fastapi import FastAPI,Query
from typing import Optional

app=FastAPI()

# query parameters

@app.get("/")
def home():
    return {"message":"Hello World"}


# default value for query parameter

@app.get("/items")
def read_items(skip:int=0,limit:int=10):
    return {"skip":skip,"limit":limit}

# required query parameter

@app.get("/users")
def read_users(q:str,age:int=10):
    return {"q":q,"age":age}

# Optional Parameters with None

@app.get("/products")
def read_products(q:Optional[str]=None):
    if q:
        return {"q":q}
    return {"message":"No query parameter provided"}


# Advance : Query Parameters

@app.get("/search")
def search_items(q:str=Query(default=None,min_length=3,max_length=50,patterns="^fixed_")):
    return {"q":q}

