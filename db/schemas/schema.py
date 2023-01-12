#db/schema/schema.py
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
  id:str
  name:str
  email:str
  password:str
  phone:str
  
  class Config:
    orm_mode = True