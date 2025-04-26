# app/auth/middleware.py

from fastapi import Request, HTTPException, status
from app.auth.jwt import verify_access_token

async def jwt_middleware(request: Request, call_next):
    if request.url.path.startswith("/auth"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

    token = auth_header.split(" ")[1] if "Bearer" in auth_header else None
    
    if not token or not verify_access_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return await call_next(request)
