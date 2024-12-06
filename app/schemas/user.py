from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for user registration. Includes password.
    """
    password: str


class UserResponse(UserBase):
    """
    Schema for the response when returning user data. Excludes sensitive fields like the password.
    """
    id: int
    is_active: bool

    class Config:
        orm_mode = True
