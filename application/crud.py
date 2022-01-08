from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas


def create_application(db: Session, application: schemas.ApplicationBase):
    application = models.Application(**application.dict())

    db.add(application)
    db.commit()
    db.refresh(application)


def get_application(db: Session, id: int):
    return db.query(models.Application).filter(models.Application.id == id).first()


def get_applications(db: Session, page: int):
    if not page:
        return db.query(models.Application).offset(0).limit(25).all()
    return db.query(models.Application).offset((page - 1) * 25).limit(25).all()


def update_application(db: Session, id: int, request: schemas.ApplicationUpdate):
    application = db.query(models.Application).filter(models.Application.id == id)
    
    if not application.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Application with id {id} not found")
    
    application.update(request.dict(exclude_unset=True), synchronize_session=False)
    db.commit()


def delete_application(db: Session, id: int):
    application = db.query(models.Application).filter(models.Application.id == id)
    
    if not application.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Application with id {id} not found")
    
    application.delete(synchronize_session=False)
    db.commit()