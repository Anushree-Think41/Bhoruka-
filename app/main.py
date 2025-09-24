from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers import user_router
import uvicorn
from app.database.db_handler import engine
from app.models.user_model import Base
from app.errors.http_error import CustomHTTPException, http_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(CustomHTTPException, http_exception_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

app.include_router(user_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)