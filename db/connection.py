#db/connection.py
from db.session import SessionLocal #방금 작성한 session에 있는 SessionLocal을 가져옵니다

def get_db():
	db = SessionLocal()
	try:
		yield db # DB 연결 성공한 경우, DB 세션 시작
	finally:
		db.close()
		# db 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.