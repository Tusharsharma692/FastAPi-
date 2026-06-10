from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from pydantic import BaseModel,EmailStr,ConfigDict
from fastapi import FastAPI,Request,Depends,HTTPException
from typing import Optional

# entry point for entering in database(like bridge)
Engine = create_engine(
    "sqlite:///./sqlAlchemyDemo.db",
    connect_args={
        "check_same_thread":False # allow other threads to access DataBase
    }
)

# Session Factory ->  whenever it's called ,it creates temporary session with DataBase
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=Engine
)

#  every model inherits Base class as parent class
Base = declarative_base()

# USER Table schema 
class USERS(Base):
    __tablename__ = "USER"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )
    name=Column(
        String
    )
    email=Column(
        String,
        unique=True
    )
    account=Column(
        Integer
    )

# TODO table schema
class TODOS(Base):

    __tablename__= "TODO"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )
    description=Column(
        String
    )

# Create all Table
Base.metadata.create_all(bind=Engine)

# Creating dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# for validation of client's data
class _user(BaseModel):
    
    name:str
    email:EmailStr
    account:int


class _responseUser(BaseModel):

    id:int
    name:str
    email:EmailStr

    model_config=ConfigDict(
        from_attributes=True
    )



class _todo(BaseModel):
    description:str

class _responseTodo(BaseModel):

    id:int
    description:str

    model_config=ConfigDict(
        from_attributes=True
    )





app=FastAPI()


@app.middleware("http")
async def basic_middleware(request:Request,call_next):
    print("Request Recevied")
    print(f"path is {request.url.path}")
    response = await call_next(request)
    print("Response Sent")

    return response




@app.get("/")
def greet(name : Optional[str]=None):  # optional query params
    if name :
        return {
            "Message":f"Welcome to FastAPI {name}! , How can i assist you ?"
        }
    return{
        "Message":"Welcome to FastAPI!"
    }


# APIS for USER's Section(CRUD)

@app.post("/user")
def create_user(user:_user,db : Session = Depends(get_db)): 


    existing_user=db.query(USERS).filter(USERS.email == user.email).first()


    if existing_user:
        raise HTTPException(
            status_code = 409,
            detail="Email already exists"
        )
    
    db_user=USERS(
        name=user.name,
        email=user.email,
        account=user.account
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "Message": "User Created Successfully",
        "Data":db_user.id
    }


   
# Get all users
@app.get("/users",response_model=list[_responseUser])
def get_user(db : Session = Depends(get_db)):
    return db.query(USERS).all()

# get user by id

@app.get("/users/{user_id}",response_model=_responseUser)
def get_user(user_id:int,db :Session = Depends(get_db)):

    user=db.query(USERS).filter(USERS.id==user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    
    return user

# Update User

@app.put("/users/{user_id}",response_model=_responseUser)
def update_user(user_id:int,updated_user:_user,db : Session = Depends(get_db)):

    user=db.query(USERS).filter(USERS.id==user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    
    user.name=updated_user.name
    user.email=updated_user.email
    user.account=updated_user.account

    db.commit()
    db.refresh(user)
    return user

# Delete USer
@app.delete("/users/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):

    user=db.query(USERS).filter(USERS.id==user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    
    db.delete(user)

    db.commit()

    return {
        "Message":"User Deleted Successfully"
    }



# TODO CRUD

# create todo

@app.post("/todos")
def create_todo(
    todo: _todo,
    db: Session = Depends(get_db)
):

    db_todo = TODOS(
        description=todo.description
    )

    db.add(db_todo)

    db.commit()

    db.refresh(db_todo)

    return {
        "Message": "Todo Created Successfully",
        "Data": db_todo.id
    }


# GET ALL TODOS
@app.get("/todos", response_model=list[_responseTodo])
def get_todos( db: Session = Depends(get_db)):

    return db.query(TODOS).all()

# GET TODO BY ID
@app.get(
    "/todos/{todo_id}",
    response_model=_responseTodo
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    todo = db.query(TODOS).filter(TODOS.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    return todo

 # UPDATE TODO
@app.put(
    "/todos/{todo_id}",
    response_model=_responseTodo
)
def update_todo(
    todo_id: int,
    updated_todo: _todo,
    db: Session = Depends(get_db)
):

    todo = db.query(TODOS).filter(TODOS.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    todo.description = updated_todo.description

    db.commit()

    db.refresh(todo)

    return todo
   
# DELETE TODO
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    todo = db.query(TODOS).filter(TODOS.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    db.delete(todo)

    db.commit()

    return {
        "Message": "Todo Deleted Successfully"
    }





