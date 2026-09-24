# CRUD-API---FlyRank

# Task CRUD API

A small REST API for managing a to-do list. It supports the four CRUD
operations — **Create, Read, Update, Delete** — over HTTP, with an
interactive Swagger UI for testing. Built as Week 2 Assignment A1 of the
FlyRank Backend Internship.

## Technologies

- **Python 3.10+**
- **FastAPI** — the web framework
- **Uvicorn** — the server that runs the app
- **Swagger UI / OpenAPI** — auto-generated interactive docs (built into FastAPI)
- **Git & GitHub** — version control and publishing

## Features

- Create, read, update and delete tasks
- Input validation (missing or empty title → `400`)
- Correct HTTP status codes: `200`, `201`, `204`, `400`, `404`
- JSON error bodies with a consistent shape: `{"error": "..."}`
- Swagger UI at `/docs` — click "Try it out" to exercise the whole API
- **In-memory storage** — a plain Python list, no database

## Installation

```bash
git clone https://github.com/<your-username>/todo-crud-api.git
cd todo-crud-api
pip install -r requirements.txt
```

## Running the API

One command:

```bash
uvicorn main:app --reload
```

Then open:

- API root: <http://localhost:8000/>
- Swagger UI: <http://localhost:8000/docs>

(`--reload` restarts the server automatically when you edit `main.py` —
remove it in "production", but for learning it is your best friend.)

## API Endpoints

| Method   | Endpoint        | Purpose             | Success code | Error codes |
|----------|-----------------|---------------------|--------------|-------------|
| GET      | `/`             | API information     | 200          | —           |
| GET      | `/health`       | Health check        | 200          | —           |
| GET      | `/tasks`        | List all tasks      | 200          | —           |
| GET      | `/tasks/{id}`   | Get one task        | 200          | 404         |
| POST     | `/tasks`        | Create a task       | 201          | 400         |
| PUT      | `/tasks/{id}`   | Update a task       | 200          | 400, 404    |
| DELETE   | `/tasks/{id}`   | Delete a task       | 204          | 404         |

Status code cheatsheet:
`200` = worked · `201` = created · `204` = worked, nothing to return ·
`400` = your request was invalid · `404` = that task does not exist.

## Example request

```bash
$ curl -i -X POST http://localhost:8000/tasks \
    -H "Content-Type: application/json" \
    -d '{"title": "Buy milk"}'

HTTP/1.1 201 Created
date: Wed, 23 Sep 2026 23:53:48 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

![Swagger UI](screenshots/swagger.png)

## A note about the data

Tasks are stored **in memory only** — a plain Python list that lives
inside the running process. Restart the server and every task is gone.
That is not a bug: it is the assignment's way of making you *feel* why
databases exist. Week 3 replaces this list with real persistent storage.

## Project structure

```text
todo-crud-api/
├── main.py              # the whole API
├── requirements.txt     # pinned dependencies
├── README.md            # this file
├── .gitignore
└── screenshots/
    └── swagger.png      # Swagger UI screenshot
```
