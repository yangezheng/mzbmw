# 🐍 FastAPI Backend – FastDev API

This is the backend for the **FastDev** fullstack template, built with **FastAPI** and managed via **Poetry**.  
It provides an API endpoint for simple calculations, and is ready to deploy on [Render](https://render.com).

---

## 🗂 Project Structure

```
fastdev/backend/
├── pyproject.toml        # Poetry config
├── poetry.lock
├── render-build.sh       # Render deployment script
├── src/
│   └── fastdev/
│       ├── main.py       # FastAPI app entrypoint
│       └── __init__.py
└── tests/                # (Optional) for test files
```

---

## 🚀 Getting Started (Local Dev)

### 1. Install dependencies

```bash
poetry install
```

### 2. Run the server locally

```bash
poetry run uvicorn backend.main:app --reload --app-dir src
```

---

## ☁️ Deployment (Render)

### 1. Create a new Web Service

- **Runtime**: Python 3.11+
- **Build command**:  
  ```bash
  poetry install
  ```
- **Start command**:  
  ```bash
  poetry run uvicorn backend.main:app --host 0.0.0.0 --port 10000 --app-dir src
  ```
- **Environment**: Add any required environment variables (if needed)

---

## ✅ Features

- ⚡ Simple REST API to handle calculation logic
- 🔁 Async support out of the box (Uvicorn + FastAPI)
- 🧪 Pythonic dev experience with Poetry
- 🔗 Easily connect with frontend via `/api/calculate`

---

## 📄 License

MIT — Use it freely, fork it, and build fast 🚀

---

## ✨ Part of the FastDev Fullstack Template