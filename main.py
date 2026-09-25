from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

# Our "database": a plain list living in memory.
# It starts with 3 example tasks and is gone when the server stops.
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": True},
]


@app.get("/", summary="API information")
def root():
    """Front door: what this API is and where its endpoints live."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health"],
    }


@app.get("/health", summary="Health check")
def health():
    """Returns ok if the server is alive. Used for monitoring."""
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    """Returns every task in the in-memory list."""
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    """Returns a single task by its id, or 404 if it does not exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    # 404 with a JSON error body: {"error": "Task 99 not found"}
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


# Shape of a valid "create task" request body
class TaskCreate(BaseModel):
    # Optional so a MISSING title also reaches our own 400 check below
    # (a required field would get FastAPI's automatic 422 instead).
    title: str | None = None


@app.post("/tasks", summary="Create a task")
def create_task(new_task: TaskCreate):
    """Adds a new task. Returns 201 + the created task, or 400 if the title is empty."""
    # Reject missing, empty, or whitespace-only titles with 400
    if new_task.title is None or not new_task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})

    # next free id = one more than the highest id currently in the list
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    return JSONResponse(status_code=201, content=task)


# Shape of a valid "update task" body: both fields optional,
# so the client may update the title, the done flag, or both.
class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, changes: TaskUpdate):
    """Applies the given title/done changes. Returns 200 + task, 404 if unknown, 400 if nothing valid to change."""
    for task in tasks:
        if task["id"] == task_id:
            # 400 if the body carries no actual changes (e.g. {} or {"title": ""})
            if changes.title is None and changes.done is None:
                return JSONResponse(status_code=400, content={"error": "Nothing to update: provide a title and/or done"})
            if changes.title is not None:
                if not changes.title.strip():
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = changes.title
            if changes.done is not None:
                task["done"] = changes.done
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.delete("/tasks/{task_id}", summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task. Success = 204 No Content (empty body); unknown id = 404."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)  # 204 = success, intentionally no body
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
