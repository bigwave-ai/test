#routes/main_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.schemas.schema import UserBase
from db.connection import get_db
from apis import user_api # main logic
from apis.auth_api import get_current_user

router = APIRouter(
    prefix="", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리
#만약 auth_routes.py라는 파일을 만들고, auth에 대한 로직을 매칭시켜놓았다고 하자. 그리고 rest 앞에 
#prefix를 /auth로 주고 싶다면 위의 prefix="/auth" 로 수정하면 됨

@router.get("/getUsers")
def get_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
	print(user)
	res = user_api.get_users(db=db) # apis 호출
	
	return {"res" : res}

