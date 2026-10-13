# main.py
# ──────────────────────────────────────────────────────────────
# Entry point of the application.
# All API routes are defined here.
# Actual database logic lives in employee_queries.py
# ──────────────────────────────────────────────────────────────

from fastapi import FastAPI, HTTPException, Query   # FastAPI core tools
from pydantic import BaseModel, EmailStr, field_validator  # for request body validation
from typing import Optional                         # for optional fields
import employee_queries                             # our SQL functions


app = FastAPI(
    title="Employee Management API",
    description="A beginner-friendly REST API built with FastAPI and MySQL",
    version="1.0.0"
)


# ── REQUEST BODY MODEL ───────────────────────────────────────
# Pydantic BaseModel defines what data the API expects in the request body.
# FastAPI uses this to automatically validate incoming JSON.
# If a field is missing or the wrong type, FastAPI returns a 422 error automatically.

class EmployeeModel(BaseModel):
    name: str           # must be a string
    email: str          # must be a string (email format)
    department: str     # must be a string
    salary: float       # must be a number

    # field_validator runs extra checks beyond just the data type
    @field_validator("name", "department")
    def must_not_be_blank(cls, value, info):
        if not value.strip():   # .strip() removes spaces — catches "   " as empty
            raise ValueError(f"{info.field_name} cannot be blank")
        return value.strip()

    @field_validator("salary")
    def salary_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Salary must be greater than 0")
        return value


# ── HEALTH CHECK ─────────────────────────────────────────────
@app.get("/")
def health_check():
    return {"message": "Employee Management API is running!"}


# ── 1. ADD EMPLOYEE ──────────────────────────────────────────
# POST /employees
# Client sends JSON body: {"name": "...", "email": "...", "department": "...", "salary": ...}
# FastAPI automatically parses and validates it using EmployeeModel

@app.post("/employees", status_code=201)
def add_employee(employee: EmployeeModel):
    """Add a new employee to the database."""
    try:
        new_id = employee_queries.add_employee(
            employee.name,
            employee.email,
            employee.department,
            employee.salary
        )
        return {
            "message": "Employee added successfully",
            "employee_id": new_id
        }

    except ValueError as error:
        # ValueError means duplicate email — 409 Conflict is the right status code
        raise HTTPException(status_code=409, detail=str(error))

    except Exception as error:
        # Any other unexpected error — 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(error))


# ── 2. GET ALL EMPLOYEES ─────────────────────────────────────
# GET /employees
# No request body needed — just call the endpoint

@app.get("/employees")
def get_all_employees():
    """Retrieve all employees from the database."""
    try:
        employees = employee_queries.get_all_employees()
        return {
            "total": len(employees),
            "employees": employees
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# ── 3. GET EMPLOYEE BY ID ────────────────────────────────────
# GET /employees/5
# {id} in the URL is a path parameter — FastAPI passes it as employee_id

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    """Retrieve a single employee by their ID."""
    try:
        employee = employee_queries.get_employee_by_id(employee_id)

        if employee is None:
            # 404 Not Found — employee with this id does not exist
            raise HTTPException(
                status_code=404,
                detail=f"Employee with id {employee_id} not found"
            )

        return employee

    except HTTPException:
        raise   # re-raise our own HTTP exceptions unchanged

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# ── 4. UPDATE EMPLOYEE ───────────────────────────────────────
# PUT /employees/5
# Client sends full updated data in the request body

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeModel):
    """Update all details of an existing employee."""
    try:
        rows_affected = employee_queries.update_employee(
            employee_id,
            employee.name,
            employee.email,
            employee.department,
            employee.salary
        )

        if rows_affected == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with id {employee_id} not found"
            )

        return {"message": f"Employee {employee_id} updated successfully"}

    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# ── 5. DELETE EMPLOYEE ───────────────────────────────────────
# DELETE /employees/5

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    """Delete an employee by their ID."""
    try:
        rows_affected = employee_queries.delete_employee(employee_id)

        if rows_affected == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with id {employee_id} not found"
            )

        return {"message": f"Employee {employee_id} deleted successfully"}

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# ── 6. SEARCH EMPLOYEES ──────────────────────────────────────
# GET /employees/search?keyword=engineering
# `keyword` is a query parameter (comes after ? in the URL)
# Query(...) means it is required — FastAPI returns 422 if it's missing

@app.get("/employees/search/query")
def search_employees(keyword: str = Query(..., min_length=1, description="Search by name or department")):
    """Search employees by name or department."""
    try:
        results = employee_queries.search_employees(keyword)
        return {
            "keyword": keyword,
            "total": len(results),
            "employees": results
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
