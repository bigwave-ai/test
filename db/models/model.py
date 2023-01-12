#db/models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from datetime import datetime

from sqlalchemy.ext.declarative import as_declarative

@as_declarative()
class Base:
    createdAt = Column(DateTime(timezone=True), default=datetime.now())
    updatedAt = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())
    __name__: str

class Users(Base):
    __tablename__ = 'users' # 필수적으로 선언 -> table의 이름

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)