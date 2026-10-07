from app.database import SessionLocal
from app.models.users import User
from app.security import hash_password

username = input("Username: ")
email = input("Email: ")
password = input("Password: ")

session = SessionLocal()

user = User(
    username=username,
    email=email,
    hashed_password=hash_password(password),
    role="admin"
)

session.add(user)
session.commit()
session.close()