from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse 
from typing import Optional
from pydantic import BaseModel, EmailStr

app=FastAPI()

USERS=[]


class user(BaseModel):
    name:str
    id:int
    Email:EmailStr

class serverResponse(BaseModel):
    name:str
    message:str

# Custom exception for user not found
class UserNotFoundException(Exception):
    def __init__(self,user_id:int):
        self.user_id=user_id


@app.exception_handler(UserNotFoundException)
def UserNotFoundHandler(request:Request,exc:UserNotFoundException):
    return JSONResponse(
        status_code = 404,
        content={
            "message":"User Not found",
            "User_id":exc.user_id
        }
    )


@app.get("/",status_code=200)
def greet(name : Optional[str]=None):
    if name:
        return {"message": f"Hello, {name}! Welcome to FastAPI."}

    return {
        "message": "Hello! Welcome to FastAPI."
    }



@app.post("/user")
def create_user(user:user):
    try:
        USERS.append(user)
        return {"message":"User created succcessfully"}
    except Exception as e:
        return {"message":f"An error occurred: {str(e)}"}
    

 
''' HTTPExceptions are used to handle errors and return appropriate HTTP status codes and messages to the client.'''

@app.get("/users/{user_id}",response_model=serverResponse)
def get_user(user_id:int):
    for user in USERS:
        if user.id == user_id:
            return serverResponse(name=user.name,message="User found")
    
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )



# using CustomException with app.exception_handler
@app.put("/users/{user_id}")
def update_user(user_id:int,updated_user:user):

    for idx,user in enumerate(USERS):
        if user.id == user_id:
            USERS[idx]=updated_user
            return {
                "message":"User successfully found and updated"
            }
    
    raise UserNotFoundException(user_id)




