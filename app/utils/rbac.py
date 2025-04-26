# app/utils/rbac.py

from fastapi import HTTPException, Depends
from app.auth.jwt import get_current_user

def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return current_user

def is_task_owner_or_admin(task_owner_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin" and current_user["user_id"] != task_owner_id:
        raise HTTPException(status_code=403, detail="Access forbidden: Not task owner or admin")
    return current_user


def is_user_or_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "user"]:
        raise HTTPException(status_code=403, detail="Access forbidden: Unauthorized role")
    return current_user
