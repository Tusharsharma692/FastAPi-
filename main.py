from fastapi import FastAPI,Request
import time

app=FastAPI()

# @app.middleware("http")
# async def my_middleWare(request:Request,call_next):
#     print("Request Received")

#     response= await call_next(request)

#     print("Response Sent")

#     return response


@app.middleware("http")
async def my_login_middleware(request:Request,call_next):
    start_time=time.time()

    response = await call_next(request)

    process_time=time.time()-start_time

    print(f"Process_Time:{process_time} and Path:{request.url.path}")

    return response
