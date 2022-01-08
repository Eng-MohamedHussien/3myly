from typing import List, Optional
from fastapi import FastAPI, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import uvicorn

from application.database import engine, SessionLocal
from application import models, schemas, crud


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/application', status_code=status.HTTP_201_CREATED)
def add_application(application: schemas.ApplicationBase, db: Session=Depends(get_db)):
    crud.create_application(db, application)
    return {'status': 'Application has been added successfully'}


@app.get('/application/{id}', response_model=schemas.Application)
def get_application(id: int, db: Session=Depends(get_db)):
    application = crud.get_application(db, id)
    
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Application with id {id} not found")
    
    return application


@app.get('/application', response_model=List[schemas.Application])
def get_applications(page: Optional[int] = None, db: Session=Depends(get_db)):
    return crud.get_applications(db, page)


@app.put('/application/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_application(id: int, request: schemas.ApplicationUpdate, db: Session=Depends(get_db)):
    crud.update_application(db, id, request)
    return {'status': f'Application with id {id} has been updated successfully'}


@app.delete('/application/{id}')
def delete_application(id: int, db: Session=Depends(get_db)):
    crud.delete_application(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)