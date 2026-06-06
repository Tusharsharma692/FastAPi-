from fastapi import FastAPI

app= FastAPI()


# home route
@app.get("/")
def home():
    return {"message": "Hello World"}


# about route

@app.get("/about")
def about():
    return {"message": "This is about page"}

# different return type
@app.get("/users")
def get_users():
    return {
        "users": [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25},
            {"name": "Doe", "age": 35}
        ]
    }

