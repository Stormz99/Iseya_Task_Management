from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwt import get_current_user
from app.database.connection import get_db
from app.schemas.task_schemas import TaskCreate, TaskResponse
from app.services.task_service import (
    create_task, 
    get_all_tasks, 
    get_task_by_id, 
    update_task, 
    delete_task
)
from app.models.enum import RoleEnum


task_router = APIRouter(tags=["Tasks"])


# CREATE TASK (Authenticated User)
@task_router.post("/", response_model=TaskResponse)
async def create_new_task(
    request: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await create_task(request, db, current_user["id"])


# RETRIEVE ALL TASKS (Admin Only)
@task_router.get("/", response_model=list[TaskResponse])
async def retrieve_all_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access only")

    return await get_all_tasks(db)


# RETRIEVE ONLY USER'S OWN TASKS (Authenticated User)
@task_router.get("/user-tasks", response_model=list[TaskResponse])
async def retrieve_user_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tasks = await get_all_tasks(db)  # Fetch all tasks
    user_tasks = [task for task in tasks if task.owner_id == current_user["id"]]
    return user_tasks


# RETRIEVE SINGLE TASK (Owner or Admin)
@task_router.get("/{task_id}", response_model=TaskResponse)
async def retrieve_task_by_id(
    task_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    task = await get_task_by_id(task_id, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user["id"] and current_user["role"] != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    return task


# UPDATE TASK (Owner or Admin)
@task_router.put("/{task_id}", response_model=TaskResponse)
async def update_task_by_id(
    task_id: int,
    request: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = await get_task_by_id(task_id, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user["id"] and current_user["role"] != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    return await update_task(task_id, request, db)


# DELETE TASK (Owner or Admin)
@task_router.delete("/{task_id}")
async def delete_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = await get_task_by_id(task_id, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user["id"] and current_user["role"] != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    return await delete_task(task_id, db)
