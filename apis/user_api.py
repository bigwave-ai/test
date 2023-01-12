# apis/user_api.py

from db.models.model import Users

def get_users(db):
  users = db.query(Users).all()
  return users