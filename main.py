from fastapi import FastAPI,Depends,Header,HTTPException

app=FastAPI()


'''
def common_logic():
    return {
        "Message":"Common Logic Executed"
    }

@app.get("/home")
def home(data = Depends(common_logic)):
    return data

@app.get("/profile")
def greet(data=Depends(common_logic)):
    return data
'''

def verify_token(token:str=Header(None)):
    if token != "mysecretToken":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return {
        "user":"Authorized User"
    }

@app.get("/secure-data")
def secure_data(user=Depends(verify_token)):
    return {
        "message":"Secure data accessed",
        "user":user
    }