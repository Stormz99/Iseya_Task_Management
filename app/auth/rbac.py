from fastapi import Depends, HTTPException, status
from app.auth.jwt import get_current_user

def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )

def is_task_owner_or_admin(task_user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin" and current_user["user_id"] != task_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
