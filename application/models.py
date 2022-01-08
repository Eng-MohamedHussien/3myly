from sqlalchemy import Column, Integer, String, Enum, Text
import enum

from .database import Base


class StateEnum(str, enum.Enum):
    ideal     = 'Ideal'
    negotiate = 'Negotiate'
    signed    = 'Signed'
    approved  = 'Approved'
    rejected  = 'Rejected'


class Application(Base):
    __tablename__ = 'applications'

    id           = Column(Integer, primary_key=True, autoincrement=True, index=True)
    client_name  = Column(String(256), nullable=False, index=True)
    client_phone = Column(String(12), nullable=False, index=True)
    product_type = Column(Text, nullable=False, index=True)
    state        = Column(Enum(StateEnum), index=True, default=StateEnum.ideal)
    notes        = Column(Text, nullable=True)