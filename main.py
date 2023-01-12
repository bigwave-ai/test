# main.py

import os
from fastapi import FastAPI
from routes.main_routes import router as main
from routes.auth_routes import router as auth

from db.models import model
from db.schemas.schema import UserBase
from db.session import  engine
from db.connection import get_db
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine) #model에 있는 구조 db에 만드는 부분

app = FastAPI() # FastAPI 모듈

#Cors정책 예외처리
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main)
app.include_router(auth)

app.include_router(SQLAlchemyCRUDRouter(schema=UserBase,create_schema=UserBase,db_model=model.Users,db=get_db))

@app.get("/") # Route Path
def index():
    return {
        "Python": "Framework",
    }