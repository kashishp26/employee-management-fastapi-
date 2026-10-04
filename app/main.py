from fastapi import FastAPI
from app.database.session import engine, Base
from app.routes import auth, department, employee
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.core.config import settings

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Employee Management REST API using FastAPI, PostgreSQL, and SQLAlchemy",
    version="1.0.0"
)

# Add Middleware
app.add_middleware(RequestLoggingMiddleware)

# Include Routers
app.include_router(auth.router)
app.include_router(department.router)
app.include_router(employee.router)

@app.get("/")
def root():
    return {"message": "Employee Management API is running! Go to /docs for Swagger UI."}