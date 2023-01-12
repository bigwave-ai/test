from db.models.model import Users
from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import jwt
from fastapi import APIRouter, HTTPException, Depends, status
from jose import JWTError
from sqlalchemy.orm import Session
from db.connection import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = "dslkfjlsdifjohi32h4oi23h4oinfldskfnoiawhefg"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def login(user, db):
  #logits
  #user가 있는지? 확인
  user =  auth_user(user.username, user.password, db)
  if not user:
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail='user not found')
  data = {'username':user.id}
  token = create_access_token(data)
  
  return {"access_token": token, "token_type": "bearer"}

def reg(user, db):
  #user 있는지 확인
  user_check = db.query(Users).filter(Users.id==user.id).first()
  if user_check:
    raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail='user exists')
  encoded_password = pwd_context.hash(user.password)
  db_user = Users(id = user.id, password = encoded_password, name=user.name, email=user.email, phone=user.phone)
  db.add(db_user)
  db.commit()

  return 'success'

def auth_user(username:str, password:str, db):
  #받은 username으로 db에서 user테이블에서 id == username인지 조회
  #만약 있다면 'user있음'이라 알린다.
  #없다면, password도 맞는지 본다.
  #다만 password는 암호화 되어 저장되 있을 거기 때문에 그거 고려해서 풀어주고(?)
  #암호화된 password와 입력받는 password가 같은지 본다.
  #그리고 같다면 user 출력 한다.
  user = db.query(Users).filter(Users.id==username).first()
  if not user:
    return False
  if not verify_password(password, user.password):
    return False
  return user
  
def verify_password(input_password, db_password):
  return pwd_context.verify(input_password, get_password_hash(db_password))

def create_access_token(data : dict):
  encoded_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_token

def decode_token(token):
  return jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_info(id, db): #this id to token
    target = db.query(Users).filter(Users.id==id).first()
    return target

async def get_current_user(token: str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username = payload.get("username")
        if username is None:
            raise credentials_exception
          
    except JWTError:
        raise credentials_exception
    user = get_user_info(username, db)
    if user is None:
        raise credentials_exception
    return user
