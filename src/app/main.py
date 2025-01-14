from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

print("Script directory:", script_dir)

app = FastAPI()

# Serve static files (HTML, CSS, JS)
#app.mount("/static", StaticFiles(directory="/app/src/static"), name="static")
app.mount("/static", StaticFiles(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))), name="static")
# Store todos
todos = []

# Pydantic model for To-Do items
class TodoItem(BaseModel):
    id: int  # Unique identifier for the to-do
    title: str  # Title or name of the task
    description: Optional[str] = None  # Optional description of the task
    done: bool = False  # Whether the task is done or not

# Endpoint to add a new to-do
@app.post("/todos/add")
def create_todo(todo: TodoItem):
    # Check if a to-do with the same ID already exists
    if any(existing_todo["id"] == todo.id for existing_todo in todos):
        raise HTTPException(
            status_code=400,
            detail=f"A to-do with ID {todo.id} already exists."
        )
    # Add the new to-do to the list
    todos.append(todo.dict())
    return {"message": "To-Do added successfully.", "todo": todo}

# Endpoint to list incomplete todos
@app.get("/todos")
def get_todos():
    incomplete_todos = [todo for todo in todos if not todo["done"]]
    return {"incomplete_todos": incomplete_todos}

# Endpoint to list only done todos
@app.get("/todos/done")
def get_done_todos():
    done_todos = [todo for todo in todos if todo["done"]]
    return {"done_todos": done_todos}

# Endpoint to list all todos (including done and incomplete)
@app.get("/todos/all")
def get_all_todos():
    return {"todos": todos}

@app.post("/todos/{id}/done")
def mark_todo_done(id: int):
    # Find the to-do with the given ID
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if not todo:
        raise HTTPException(
            status_code=404, detail=f"To-Do with ID {id} not found."
        )
    # Update the to-do with the new status
    todo["done"] = True
    return {"message": "To-Do marked as done.", "todo": todo}

# Endpoint to delete a to-do
@app.delete("/todos/{id}")
def delete_todo(id: int):
    # Find the to-do with the given ID
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if not todo:
        raise HTTPException(
            status_code=404, detail=f"To-Do with ID {id} not found."
        )
    # Remove the to-do from the list
    todos.remove(todo)
    return {"message": "To-Do deleted successfully.", "todo": todo}

# Serve the main HTML page
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Open the index.html file from the static directory (docker filesystem "overlay2" doesnt like "../" by itself)
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/index.html")), "r") as f:
        return f.read()


script_dir = os.path.dirname(os.path.abspath(__file__))

print("Script directory:", script_dir)
