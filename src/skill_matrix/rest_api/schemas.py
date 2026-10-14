from pydantic import BaseModel, EmailStr
from typing import Optional

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

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role_id: int | None = None
    department: str | None = None

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None

class SkillResponse(SkillBase):
    skill_id: int
    class Config:
        from_attributes = True 


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    manager_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    project_id: int
    title: str
    description: str | None
    manager_id: int
    class Config:
        from_attributes = True

