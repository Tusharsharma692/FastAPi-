from fastapi import FastAPI
from pydantic import BaseModel,EmailStr

class user(BaseModel):
    id:int
    name:str
    emal:EmailStr


users=[]
app=FastAPI()

@app.post("/user")
def create_user(user:user):
    try:
        users.append(user)

        return {
            "Message":"User created successfully",
            "Data":user
        }
    except Exception as e:
        return {
            "Message":"Error creating user",
            "Error":str(e)
        }
    

@app.put("/user/{user_id}")
def update_user(user_id:int,user:user,notify:bool=False): 
    
    ''' notify is an optional query parameter to indicate whether to send a notification after updating the user'''

    for idx,usr in enumerate(users):
        if usr.id == user_id:
            users[idx]=user
            if notify:
                return {
                    "Message":"User updated successfully and notification sent",
                    "Data":users
                }
            return {
                "Message":"User updated successfully",
                "Data":users
            }