from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

lists=[]

class user(BaseModel):
    id:int
    name:str
    email:EmailStr
    password:int


class serverResponse(BaseModel):
    id:int
    name:str
    email:EmailStr

app=FastAPI()

@app.get("/")
def greet(name:Optional[str]=None):

    if name:
        return {
            "Message":f"Hello {name}! welcome to FastAPI"
        }
    return{
        "Message":"Hello! welcome to FastAPI"
    }


@app.post("/users")
def create_user(user:user):
    try:
        lists.append(user)
        return {
            "Message":"User created successfully",
            "Data":user
        }
    except Exception as e:
        return {
            "Message":"Error creating user",
            "Error":str(e)
        }
    


'''The password field is automatically removed because it is not part of ServerResponse. This is one of the main uses of response_model.
'''


'''
 return {
            "Message":"User not found"
        }

        we can't use this response because it doesn't match the response_model. 


'''
@app.get("/users",response_model=serverResponse)
def get_user(user_id:int):
    for user in lists:
        if user.id==user_id:
            return user
    
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
    

