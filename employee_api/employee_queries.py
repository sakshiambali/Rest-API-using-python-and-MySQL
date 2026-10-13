# employee_queries.py
# ──────────────────────────────────────────────────────────────
# This file contains all SQL query functions for employee operations.
# main.py will import and call these functions.
# Keeping SQL here makes main.py clean and readable.
# ──────────────────────────────────────────────────────────────

from database import get_connection     # our function that opens a MySQL connection
import mysql.connector                  # needed to catch MySQL-specific errors


# ── 1. ADD EMPLOYEE ──────────────────────────────────────────
def add_employee(name, email, department, salary):
    """
    Inserts a new employee row into the employees table.
    Returns the auto-generated id of the new employee.
    """
    connection = None   # we set this to None so the finally block is safe
    cursor = None

    try:
        connection = get_connection()

        # A cursor is like a pen that writes/reads from the database.
        # dictionary=True makes rows come back as dicts like {"id": 1, "name": "Ravi"}
        # instead of plain tuples like (1, "Ravi")
        cursor = connection.cursor(dictionary=True)

        # %s are placeholders — mysql.connector replaces them safely with real values.
        # This prevents SQL Injection attacks (never use f-strings inside SQL).
        sql = """
            INSERT INTO employees (name, email, department, salary)
            VALUES (%s, %s, %s, %s)
        """
        values = (name, email, department, salary)

        cursor.execute(sql, values)

        # commit() saves the INSERT permanently to the database.
        # Without commit(), the data is lost when the connection closes.
        connection.commit()

        # cursor.lastrowid gives the auto-generated id of the row just inserted
        return cursor.lastrowid

    except mysql.connector.IntegrityError:
        # IntegrityError happens when a UNIQUE constraint is violated
        # i.e., someone tries to add an employee with an email that already exists
        raise ValueError(f"Email '{email}' already exists in the database.")

    except mysql.connector.Error as error:
        raise Exception(f"Database error while adding employee: {error}")

    finally:
        # finally always runs — even if an exception occurred.
        # We use it to close the cursor and connection so we don't leak resources.
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ── 2. GET ALL EMPLOYEES ─────────────────────────────────────
def get_all_employees():
    """
    Returns a list of all employees from the database.
    Each employee is a dictionary: {"id": 1, "name": "Ravi", ...}
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        sql = "SELECT * FROM employees ORDER BY id ASC"
        cursor.execute(sql)

        # fetchall() returns a list of all matching rows
        employees = cursor.fetchall()
        return employees

    except mysql.connector.Error as error:
        raise Exception(f"Database error while fetching employees: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ── 3. GET EMPLOYEE BY ID ────────────────────────────────────
def get_employee_by_id(employee_id):
    """
    Returns a single employee dict matching the given id.
    Returns None if no employee found with that id.
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        sql = "SELECT * FROM employees WHERE id = %s"
        cursor.execute(sql, (employee_id,))

        # fetchone() returns one row, or None if nothing matched
        employee = cursor.fetchone()
        return employee

    except mysql.connector.Error as error:
        raise Exception(f"Database error while fetching employee: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ── 4. UPDATE EMPLOYEE ───────────────────────────────────────
def update_employee(employee_id, name, email, department, salary):
    """
    Updates all fields of an employee with the given id.
    Returns the number of rows affected (0 means employee not found).
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        sql = """
            UPDATE employees
            SET name = %s, email = %s, department = %s, salary = %s
            WHERE id = %s
        """
        values = (name, email, department, salary, employee_id)

        cursor.execute(sql, values)
        connection.commit()

        # cursor.rowcount tells how many rows were changed
        # If it's 0, no employee with that id was found
        return cursor.rowcount

    except mysql.connector.IntegrityError:
        raise ValueError(f"Email '{email}' already belongs to another employee.")

    except mysql.connector.Error as error:
        raise Exception(f"Database error while updating employee: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ── 5. DELETE EMPLOYEE ───────────────────────────────────────
def delete_employee(employee_id):
    """
    Deletes the employee with the given id.
    Returns the number of rows deleted (0 means employee not found).
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        sql = "DELETE FROM employees WHERE id = %s"
        cursor.execute(sql, (employee_id,))
        connection.commit()

        return cursor.rowcount

    except mysql.connector.Error as error:
        raise Exception(f"Database error while deleting employee: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ── 6. SEARCH EMPLOYEES ──────────────────────────────────────
def search_employees(keyword):
    """
    Returns employees whose name OR department contains the keyword.
    Search is case-insensitive thanks to LIKE and % wildcards.
    Example: keyword="eng" matches "Engineering", "Senior Engineer"
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # LIKE '%eng%' matches anything containing "eng" anywhere in the text
        # We search both name and department columns
        sql = """
            SELECT * FROM employees
            WHERE name LIKE %s OR department LIKE %s
            ORDER BY id ASC
        """
        # We wrap keyword with % on both sides to search anywhere in the string
        pattern = f"%{keyword}%"
        cursor.execute(sql, (pattern, pattern))

        results = cursor.fetchall()
        return results

    except mysql.connector.Error as error:
        raise Exception(f"Database error while searching employees: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
