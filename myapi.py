from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class todoApp(BaseModel):
    title : str
    description : str
    status : str
    
class updateTodo(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = None
    
class user(BaseModel):
    auth : str
    name : str
    email : str
    
class updateUser(BaseModel):
    auth : Optional[str] = None
    name : Optional[str] = None
    email : Optional[str] = None
    
todo = {
    1 : todoApp(
        title = "WADS Assignment",
        description = "Create FastAPI Design",
        status = "incomplete",
    ),
    
    2 : todoApp(
        title = "Compnet Assignment",
        description = "Finish GNS3",
        status = "completed",
    )
}

users = {
    1 : user(
        auth = "google",
        name = "Ferdinand",
        email = "ferdinand@gmail.com",
    ),
    
    2 : user(
        auth = "local",
        name = "Jacques",
        email = "jacques@gmail.com",
    )
}

@app.get("/")
def index():
    return {"FastAPI Assignment" : "TodoApp"}

@app.get("/get-all-users")
def get_all_users():
    return users

@app.get("/get-user-by-auth/{auth}")
def get_user_by_auth(auth : str = Path(description = "The authentication method you want to view")):
    for users_id in users:
        if users[users_id].auth == auth.lower():
            return users[users_id]
    
    return {"Error" : "Invalid Authentication"}

@app.get("/get-user-by-id/{users_id}")
def get_user_by_id(users_id : int = Path(description = "The ID of user you want to view")):
    return users[users_id]

@app.get("/get-user-by-name/{name}")
def get_user_by_name(name : str = Path(description = "The name of user you want to view")):
    for users_id in users:
        if users[users_id].name.lower() == name.lower():
            return users[users_id]
    
    return {"Error" : "User not found"}

@app.get("/get-all-todo")
def get_all_todo():
    return todo

@app.get("/get-todo-by-id/{todo_id}")
def get_todo_by_id(todo_id : int = Path(description = "The ID of todo you want to view")):
    return todo[todo_id]

@app.get("/get-todo-by-title/{title}")
def get_todo_by_title(title : str = Path(description = "The title of todo you want to view")):
    for todo_id in todo:
        if todo[todo_id].title.lower() == title.lower():
            return todo[todo_id]
    
    return {"Error" : "Todo not found"}

@app.get("/get-todo-by-status/{status}")
def get_todo_by_status(status : str = Path(description = "The status of todo you want to view")):
    for todo_id in todo:
        if todo[todo_id].status.lower() == status.lower():
            return todo[todo_id]
        
    return {"Error" : "Invalid Status"}

@app.post("/create-user/{users_id}")
def create_user(users_id : int, user : user):
    if users_id in users:
        return {"Error" : "User exists"}
    
    users[users_id] = user
    return users[users_id]

@app.post("/create-todo/{todo_id}")
def create_todo(todo_id : int, todos : todoApp):
    if todo_id in todo:
        return {"Error" : "Todo exists"}
    
    todo[todo_id] = todos
    return todo[todo_id]

@app.put("/update-user/{users_id}")
def update_user(users_id : int, user : updateUser):
    if users_id not in users:
        return {"Error" : "User not found"}
    
    if user.auth != None:
        users[users_id].auth = user.auth
    if user.name != None:
        users[users_id].name = user.name
    if user.email != None:
        users[users_id].email = user.email
    return users[users_id]

@app.put("/update-todo/{todo_id}")
def update_todo(todo_id : int, todos : updateTodo):
    if todo_id not in todo:
        return {"Error": "Todo not found"}
    
    if todos.title != None:
        todo[todo_id].title = todos.title
    if todos.description != None:
        todo[todo_id].description = todos.description
    if todos.status != None:
        todo[todo_id].status = todos.status

    return todo[todo_id]

@app.delete("/delete-user/{users_id}")
def delete_user(users_id : int):
    if users_id not in users:
        return {"Error" : "User not found"}
    
    del users[users_id]
    return {"Message" : "User deleted successfully"}

@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id : int):
    if todo_id not in todo:
        return {"Error" : "Todo not found"}
    
    del todo[todo_id]
    return {"Message": "Todo deleted successfully"}