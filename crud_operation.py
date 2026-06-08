from fastapi import FastAPI
from pydantic import BaseModel

class activity(BaseModel):
    id:int
    name:str
    description:str

app=FastAPI()

todos_List=[]

# get API
@app.get("/todos")
def get_todos():
    return{
        "Message":"List of all todos",
        "Data":todos_List
    }

@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todos_List:
        if todo.id==todo_id:
            return{
                "Message":"Todo found",
                "Data":todo
            }
        return {
            "Message":"Todo not found"
        }
    

# post API
@app.post("/todos")
def create_todo(activity:activity):
    try:
        todos_List.append(activity)
        return {
            "Message":"Todo created successfully",
            "Data":activity
        }
    except Exception as e:
        return {
            "Message":"Error creating todo",
            "Error":str(e)
        }
    

# update API
@app.put("/todos/{todo_id}")
def update_todo(todo_id:int,activity:activity):
    for idx,todo in enumerate(todos_List):
        if todo.id == todo_id:
            todos_List[idx]=activity
            return {
                "Message":"Todo updated successfully",
                "Data":todos_List
            } 

    return {
        "Message":"Todo not found"
    }


# delete API
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for idx,todo in enumerate(todos_List):
        if todo.id==todo_id:
            todos_List.pop(idx)
            return{
                "Message":"Todo deleted successfully",
                "Data":todos_List
            }
        return {
            "Message":"Todo not found"
        }

