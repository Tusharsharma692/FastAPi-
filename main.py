from jose import jwt 
from datetime import datetime, timedelta, timezone
import secrets
from fastapi import FastAPI, HTTPException, Header, Depends

SECRET_KEY = secrets.token_hex(32)
algorithm = "HS256"

app=FastAPI()


# create token
def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=algorithm  
    )
    return token

# Login api(Token Genrate)
@app.post("/login")
def login(username:str,password:str):
    if username != "admin" or password != "admin123":
        raise HTTPException(
            status_code =401,
            detail="Invalid Username/Password"
        )
    
    token=create_token({
        "sub":username
    })
    return{
        "access token":token
    }

# Token Varification
def varify_token(token:str=Header(None)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=algorithm)
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    

# protected_Route
@app.get("/secure")
def secure_data(user=Depends(varify_token)):
    return {
        "Message":"Secure Data Accessed",
        "user":user
    }



