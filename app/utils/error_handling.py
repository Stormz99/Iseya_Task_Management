# app/utils/error_handling.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.response import error_response

# Handler for 400 Bad Request error
async def handle_400_error(request: Request, exc: HTTPException):
    return JSONResponse(
        content=error_response(message="Bad Request", status_code=400),
        status_code=400
    )

# Handler for 401 Unauthorized error
async def handle_401_error(request: Request, exc: HTTPException):
    return JSONResponse(
        content=error_response(message="Unauthorized", status_code=401),
        status_code=401
    )

# Handler for 404 Not Found error
async def handle_404_error(request: Request, exc: HTTPException):
    return JSONResponse(
        content=error_response(message="Not Found", status_code=404),
        status_code=404
    )

# Handler for 500 Internal Server Error
async def handle_500_error(request: Request, exc: Exception):
    return JSONResponse(
        content=error_response(message="Internal Server Error", status_code=500),
        status_code=500
    )
