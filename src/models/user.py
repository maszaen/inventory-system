from typing import Optional
from datetime import datetime
from bson import ObjectId
import bcrypt
from src.database.connection import DatabaseConnection


class User:
    def __init__(
        self,
        username: str,
        password: str,  # Hashed password
        full_name: str,
        role: str = "user",
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role
        self.created_at = created_at or datetime.utcnow()

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class UserManager:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        self.collection = self.db.get_collection("users")

    def create_user(
        self, username: str, password: str, full_name: str, role: str = "user"
    ) -> Optional[User]:
        if self.get_user_by_username(username):
            raise ValueError("Username already exists")

        hashed_password = User.hash_password(password).decode("utf-8")
        user = User(username, hashed_password, full_name, role)

        result = self.collection.insert_one(
            {
                "_id": user._id,
                "username": user.username,
                "password": user.password,
                "full_name": user.full_name,
                "role": user.role,
                "created_at": user.created_at,
            }
        )

        return user if result.inserted_id else None

    def get_user_by_username(self, username: str) -> Optional[User]:
        user_data = self.collection.find_one({"username": username})
        if user_data:
            return User(
                username=user_data["username"],
                password=user_data["password"],
                full_name=user_data["full_name"],
                role=user_data["role"],
                _id=user_data["_id"],
                created_at=user_data["created_at"],
            )
        return None

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
