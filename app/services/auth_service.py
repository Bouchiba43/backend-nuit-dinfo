from app.models.user import User
from app.utils.hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

class AuthService:
    @staticmethod
    def authenticate_user(db, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    @staticmethod
    def register_user(db, user_data):
        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pwd,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
