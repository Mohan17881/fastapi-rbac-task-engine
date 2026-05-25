from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db_config.db import get_db, Task
from schemas.schemas import TaskCreate, TaskResponse
from core.dependencies import get_current_user

router = APIRouter(tags=["Task Management"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        owner_id=current_user["id"]
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[TaskResponse])
def get_my_tasks(
    status_filter: str | None = None,  
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.owner_id == current_user["id"])
    
    if status_filter:
        query = query.filter(Task.status == status_filter)
        
    return query.all()

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    
    task.title = task_in.title
    task.description = task_in.description
    task.status = task_in.status
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    
    db.delete(task)
    db.commit()
    return None
