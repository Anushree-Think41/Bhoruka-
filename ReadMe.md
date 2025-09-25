# Bhoruka Backend

This project is a FastAPI application that provides basic user registration and login functionality.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Psycopg2](https://www.psycopg.org/docs/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Passlib](https://passlib.readthedocs.io/en/stable/)
- [Python-JOSE](https://python-jose.readthedocs.io/en/latest/)
- [Pytest](https://docs.pytest.org/en/7.1.x/)
- [HTTPX](https://www.python-httpx.org/)

## Project Structure

```
/
├── alembic.ini
├── note.md
├── ReadMe.md
├── requirements.txt
├── alembic/
└── app/
    ├── main.py
    ├── database/
    ├── errors/
    ├── models/
    ├── routers/
    ├── schemas/
    └── services/
```

## API Endpoints

The following endpoints are available:

- `POST /users/`: Create a new user.
- `POST /users/token`: Log in and get an access token.
- `GET /users/me`: Get the current user's details.
- `GET /users/{user_id}`: Get a user's details by ID.


#### OWNER

- `POST /owners`: Create a new owners.
- `GET /owners`: Get owners's details.
- `GET /owners/{owner_id}`: Get a owner's details by ID.
- `GET /owners/{owner_id}/establishments`: Get a owner's establishments by ID.

#### ESTABLISHMENTS

- `POST /establishments/`: Create a new establishment.
- `GET /establishments/`: Get all establishments.
- `GET /establishments/{establishment_id}`: Get an establishment's details by ID.
- `PUT /establishments/{establishment_id}`: Update an establishment's details by ID.
- `DELETE /establishments/{establishment_id}`: Delete an establishment by ID.


## Authentication

This application uses JSON Web Tokens (JWT) for authentication.

To authenticate, send a `POST` request to the `/users/token` endpoint with the user's email and password in the request body (as form data).

The server will respond with an access token.

Include this token in the `Authorization` header of subsequent requests as a Bearer token:

```
Authorization: Bearer <your-token>
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Anushree-Think41/Bhoruka-.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up the database:
    - Create a PostgreSQL database.
    - Create a `.env` file in the root directory and add the following environment variables:
      ```
      DATABASE_URL="postgresql://user:password@host:port/database_name"
      SECRET_KEY="your-secret-key"
      ALGORITHM="your-algorithm"
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      ```
    - Run the database migrations:
      ```bash
      alembic upgrade head
      ```

### Running the application

```bash
uvicorn app.main:app --reload
```

The application will be running at `http://localhost:8000`.