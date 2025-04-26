from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.task import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse


async def create_task(request: TaskCreate, db: AsyncSession, user_id: int) -> TaskResponse:
    """Create a new task for a user and return as TaskResponse."""
    try:
        new_task = Task(**request.dict(), owner_id=user_id)
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return TaskResponse.from_orm(new_task)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_all_tasks(db: AsyncSession) -> list[TaskResponse]:
    """Retrieve all tasks (Admin only) and return as a list of TaskResponse."""
    try:
        result = await db.execute(select(Task))
        tasks = result.scalars().all()
        return [TaskResponse.from_orm(task) for task in tasks]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")


async def get_task_by_id(task_id: int, db: AsyncSession) -> TaskResponse:
    """Retrieve a single task by ID and return as TaskResponse."""
    try:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.from_orm(task)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task: {str(e)}")


async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession) -> TaskResponse:
    """Update a task (only by owner or admin) and return as TaskResponse."""
    try:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)
        return TaskResponse.from_orm(task)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


async def delete_task(task_id: int, db: AsyncSession) -> dict:
    """Delete a task (only by owner or admin)."""
    try:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        await db.delete(task)
        await db.commit()
        return {"detail": "Task deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")
