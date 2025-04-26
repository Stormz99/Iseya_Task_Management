from fastapi import FastAPI, Request, Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.routes.task_routes import task_router
from app.routes.auth_routes import auth_router
from app.auth.middleware import jwt_middleware
from app.utils.error_handling import handle_400_error, handle_401_error, handle_404_error, handle_500_error
from app.init_db import create_db_and_tables

# **Use OAuth2PasswordBearer for Bearer Token Auth in Swagger**
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="Iseya Task Management API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Handles user authentication (login, register)",
        },
        {
            "name": "Tasks",
            "description": "Manages tasks (create, retrieve, update, delete)",
        },
    ],
    swagger_ui_parameters={"persistAuthorization": True}
)

# ** Swagger UI to Use Bearer Token Instead of Username/Password**
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Iseya Task Management API",
        version="1.0.0",
        description="API for managing tasks with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Root Route
@app.get("/")
async def root():
    return {"message": "Welcome to Iseya Task Management API"}

# JWT Middleware
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    public_routes = ["/", "/docs", "/openapi.json", "/auth/login", "/auth/register"]

    if any(request.url.path.startswith(route) for route in public_routes):
        return await call_next(request)

    return await jwt_middleware(request, call_next)

# Register Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

# Error Handlers
app.add_exception_handler(400, handle_400_error)
app.add_exception_handler(401, handle_401_error)
app.add_exception_handler(404, handle_404_error)
app.add_exception_handler(500, handle_500_error)

# Run the function to create ENUM and tables
@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()
