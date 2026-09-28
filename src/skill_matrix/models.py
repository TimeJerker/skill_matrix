from typing import List
from sqlalchemy import String, ForeignKey,Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Role(Base):
    __tablename__ = "role"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

    users: Mapped[List["User"]] = relationship(back_populates="role")

class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("role.role_id"), nullable=False)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(20))
    department: Mapped[str] = mapped_column(Text)

    role: Mapped["Role"] = relationship(back_populates="users")
    user_skills: Mapped[List["UserSkill"]] = relationship(back_populates="user")
    project_memberships: Mapped[List["ProjectMember"]] = relationship(back_populates="user")
    managed_projects: Mapped[List["Project"]] = relationship(back_populates="manager",foreign_keys="Project.manager_id")

class Skill(Base):
    __tablename__ = "skill"

    skill_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(20))

    user_skills: Mapped[List["UserSkill"]] = relationship(back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skill"

    level: Mapped[int] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skill.skill_id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="user_skills")
    skill: Mapped["Skill"] = relationship(back_populates="user_skills")

class Project(Base):
    __tablename__ = "project"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text)

    manager_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)

    members: Mapped[List["ProjectMember"]] = relationship(back_populates="project")
    manager: Mapped["User"] = relationship(back_populates="managed_projects", foreign_keys=[manager_id])


class ProjectMember(Base):
    __tablename__ = "project_member"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.project_id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="project_memberships")
    project: Mapped["Project"] = relationship(back_populates="members")
