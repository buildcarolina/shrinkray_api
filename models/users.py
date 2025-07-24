from sqlmodel import SQLModel, Field, Column, String, UniqueConstraint
from pydantic import EmailStr
from uuid import UUID, uuid4
import bcrypt

class User(SQLModel):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(sa_column=Column(String(225), unique=True))
    hashed_password: str = Field(sa_column=Column(String))

    UniqueConstraint("email", name="uq_user_email")

    def __repr__(self):
        """
        Returns string representation of model instance
        !r means the value is formatted using its
        __repr__ method rather than its __str__ method.
        """
        return f"<User {self.email!r}>"

    @staticmethod
    def hash_password(password) -> str:
        """
        Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def validate_password(self, pwd) -> bool:
        return bcrypt.checkpw(password=pwd.encode(), hashed_password=self.hashed_password.encode())

class UserBaseSchema(User):
    pass


class UserSchema(UserBaseSchema):
    class Config:
        populate_by_name = True

class UserAccountSchema(UserBaseSchema):
    """ We set an alias for the field so that when this field is serialized or deserialized,
    the name "password" will be used instead of "hashed_password." """
    hashed_password: str = Field(alias="password")
