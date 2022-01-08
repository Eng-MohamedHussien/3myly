from pydantic import BaseModel
from typing import Optional

from .models import StateEnum


class ApplicationBase(BaseModel):
    client_name : str
    client_phone: str
    product_type: str


class Application(ApplicationBase):
    id   : int
    state: str
    notes: Optional[str]

    class Config:
        orm_mode = True


class ApplicationUpdate(BaseModel):
    client_name : Optional[str] = None
    client_phone: Optional[str] = None
    product_type: Optional[str] = None
    state       : Optional[StateEnum] = None
    notes       : Optional[str] = None