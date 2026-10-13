# Employee Management API

A beginner-friendly REST API built with **Python**, **FastAPI**, and **MySQL**.

---

## Project Structure

```
employee_api/
├── main.py               # FastAPI app entry point, all routes registered here
├── database.py           # MySQL connection logic
├── employee_queries.py   # SQL query functions for employee operations
├── file_operations.py    # File handling helper functions
├── uploads/              # Uploaded files are saved here
├── reports/              # Exported CSV/JSON files are saved here
├── requirements.txt      # Project dependencies
├── .env                  # Secret credentials (never commit to GitHub)
└── README.md             # This file
```

---

## Prerequisites

- Python 3.10 or higher
- MySQL 8.0 or higher
- VS Code
- Postman (for API testing)

---

## Setup Instructions

### 1. Create and activate a virtual environment

```powershell
# Inside the employee_api folder
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Open `.env` and replace `your_mysql_password_here` with your actual MySQL password.

### 4. Create the MySQL database

Log in to MySQL and run:

```sql
CREATE DATABASE employee_db;
```

### 5. Run the API server

```powershell
uvicorn main:app --reload
```

### 6. Open the interactive API docs

Visit: http://127.0.0.1:8000/docs

---

## API Endpoints (added stage by stage)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |

More endpoints will be added in later stages.
