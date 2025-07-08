#from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from model import UpdateTaskModel, Tasks, CreateTask

app = FastAPI()

#setup db tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#rest of the code: endpoints etc.
@app.post('/createTask', status_code=201)
async def createTask(task: CreateTask, db: Session = Depends(get_session)):
    new_task = Tasks(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get('/getAllTasks', status_code=200)
async def getAllTasks(db: Session = Depends(get_session)):
    tasks = db.exec(select(Tasks)).all()
    return tasks

@app.patch('/updateTask/{task_id}', status_code=200)
async def updateTask(task_id : int, task : UpdateTaskModel, db: Session = Depends(get_session)):
    taskToUpdate = db.get(Tasks, task_id)
    taskUpdateData = task.model_dump(exclude_unset=True)
    if not taskToUpdate:
        raise HTTPException(
            status_code=400,
            detail=f"Task with id {task_id} not found"
        )
    taskToUpdate.sqlmodel_update(taskUpdateData)
    db.add(taskToUpdate)
    db.commit()
    db.refresh(taskToUpdate)
    return taskToUpdate

@app.delete('/deleteTask/{task_id}', status_code=200)
async def deleteTask(task_id : int, task : Tasks, db: Session = Depends(get_session)):
    taskToDelete = db.get(Tasks, task_id)
    if not taskToDelete:
        raise HTTPException(
            status_code=400,
            detail=f"Task with id {task_id} not found"
        )
    db.delete(taskToDelete)
    db.commit()
    return {"ok": True}