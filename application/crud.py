from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional

from sqlalchemy.sql.functions import mode

from . import models, schemas


def create_application(db: Session, application: schemas.ApplicationBase):
    application = models.Application(**application.dict())

    db.add(application)
    db.commit()
    db.refresh(application)


def get_application(db: Session, id: int):
    return db.query(models.Application).filter(models.Application.id == id).first()


def get_applications(db: Session, phone: str, name: str, state: schemas.StateEnum, page: int):
    offset = 0
    limit = 25

    if page:
        offset = (page - 1) * 25

    if not phone:
        if name:
            if not state:
                return db.query(models.Application).filter(models.Application.client_name.contains(name))\
                                                   .offset(offset).limit(limit).all()
            else:
                return db.query(models.Application).filter(models.Application.client_name.contains(name),\
                                                           models.Application.state == state)\
                                                   .offset(offset).limit(limit).all()
        else:
            if not state:
                return db.query(models.Application).offset(offset).limit(limit).all()
            else:
                return db.query(models.Application).filter(models.Application.state == state)\
                                                   .offset(offset).limit(limit).all()
    else:
        if not state:
            return db.query(models.Application).filter(models.Application.client_phone == phone)\
                                               .offset(offset).limit(limit).all()
        else:
            return db.query(models.Application).filter(models.Application.client_phone == phone,\
                                                       models.Application.state == state)\
                                               .offset(offset).limit(limit).all()


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