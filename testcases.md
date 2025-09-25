# User Module Test Cases

This document outlines the test cases for the user authentication and management module of the Bhoruka Backend application.

## Test File Location

The test cases are located in the following file:
`Test/test_user_module.py`

## Test Cases Covered

The test suite covers the following functionalities:

1.  **User Creation:**
    *   Successful creation of a new user.
    *   Attempting to create a user with an already registered email (expected to fail).

2.  **User Login:**
    *   Successful user login and access token generation.
    *   Attempting to log in with an incorrect password (expected to fail).
    *   Attempting to log in with an unregistered email (expected to fail).

3.  **Get Current User (`/users/me`):**
    *   Retrieving details of the currently authenticated user with a valid token.
    *   Attempting to retrieve current user details without authentication (expected to fail).

4.  **Get User by ID (`/users/{user_id}`):**
    *   Retrieving details of a user by a valid ID.
    *   Attempting to retrieve details for a non-existent user ID (expected to fail).

## How to Run Tests

To run these test cases, navigate to the root directory of your project (`/home/think-41-gf-5g/Bhoruka-Backend/`) in your terminal and execute the following command:

```bash
PYTHONPATH=. pytest Test/test_user_module.py
```

**Explanation of the command:**
*   `PYTHONPATH=.`: This sets the `PYTHONPATH` environment variable to the current directory. This is crucial for Python to correctly locate the `app` package and its modules (e.g., `app.main`, `app.models.user_model`).
*   `pytest`: This invokes the `pytest` test runner, which discovers and executes the tests.
*   `Test/test_user_module.py`: This specifies the path to the test file you want to execute.

## Test Environment

The tests are configured to use an in-memory SQLite database (`sqlite:///./test.db`). This ensures that each test run is isolated and does not interfere with your main development database. Database tables (`User` and `Owner`) are created and dropped for each test session to maintain a clean state.

## Note on `ARRAY` Type Error

During the initial test run setup, an `UnsupportedCompilationError` related to the `ARRAY` data type was encountered. This is because SQLite does not natively support PostgreSQL's `ARRAY` type, which was used in the `Establishment` model. To resolve this for the user module tests (which do not directly depend on the `Establishment` model), the test setup was modified to explicitly create and drop only the `User` and `Owner` tables, bypassing the `Establishment` table creation in the SQLite test database.



# Owner Module Test Cases
