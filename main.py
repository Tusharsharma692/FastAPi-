from fastapi import FastAPI,Path
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app=FastAPI()

# Path parameters

@app.get("/")
def home_page():
    return {"Message":"Welcome to FastAPI"}


# 1. Basic path parameter

@app.get("/users/{user_id}")
def get_user(user_id):
    return {"User ID":user_id}

# 2. Path parameter with type conversion

@app.get("/items/{item_id}")
def get_item(item_id:int):
    return {"Item ID":item_id}

# 3. Multiple path parameters
@app.get("/orders/{order_id}/items/{item_id}")
def get_order_item(order_id:int, item_id:int):
    return {"Order ID":order_id, "Item ID":item_id}

# 4 Advance path validation
@app.get("/products/{product_id}")
def get_product(
    product_id:int = Path(title="Product ID", description="The ID of the product to retrieve", gt=0, lt=100)
):
    return {"Product ID":product_id}

# 5. Path Paramter containing Paths

@app.get("/files/{file_path:path}")
def get_file(file_path:str):
    return {"File Path":file_path}

# 6 with enum

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    return {"model_name": model_name, "message": "Have some residuals"}



