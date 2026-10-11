from pydantic import BaseModel, EmailStr

class RoleResponse(BaseModel):
    role_id: int
    name: str

    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: int
    department: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role_id: int
    department: str | None

    class Config:
        from_attributes = True