#routes/main_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.schemas.schema import UserBase
from db.connection import get_db
from apis import auth_api # main logic
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리
#만약 auth_routes.py라는 파일을 만들고, auth에 대한 로직을 매칭시켜놓았다고 하자. 그리고 rest 앞에 
#prefix를 /auth로 주고 싶다면 위의 prefix="/auth" 로 수정하면 됨


class Token(BaseModel):
    access_token: str
    token_type: str

@router.post('/reg')
def reg(user:UserBase, db:Session=Depends(get_db)):
  result = auth_api.reg(user, db)
  return result

@router.post('/login', response_model=Token)
async def login(user:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
  result = auth_api.login(user, db)
  return result
