from typing import List
from sqlalchemy import String, ForeignKey, ForeignKeyConstraint, Text, BigInteger
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
    role_role_id: Mapped[int] = mapped_column(ForeignKey("role.role_id"), primary_key=True)

    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(20))
    department: Mapped[str] = mapped_column(Text)

    role: Mapped["Role"] = relationship(back_populates="users")
    user_skills: Mapped[List["UserSkill"]] = relationship(back_populates="user")
    project_memberships: Mapped[List["ProjectMember"]] = relationship(back_populates="user")

class Skill(Base):
    __tablename__ = "skill"

    skill_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(20))

    user_skills: Mapped[List["UserSkill"]] = relationship(back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skill"

    level: Mapped[int] = mapped_column()

    skill_skill_id: Mapped[int] = mapped_column(ForeignKey("skill.skill_id"), primary_key=True)
    user_user_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_user_id", "role_id"],         
            ["user.user_id", "user.role_role_id"]
        ),
    )

    user: Mapped["User"] = relationship(back_populates="user_skills")
    skill: Mapped["Skill"] = relationship(back_populates="user_skills")

class Project(Base):
    __tablename__ = "project"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text)

    user_user_id: Mapped[int] = mapped_column()
    manager_id: Mapped[int] = mapped_column()
    role_id: Mapped[int] = mapped_column()

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_user_id", "role_id"],
            ["user.user_id", "user.role_role_id"],
            name="Project_user_fk"
        ),  
    )

    members: Mapped[List["ProjectMember"]] = relationship(back_populates="project")

class ProjectMember(Base):
    __tablename__ = "project_member"

    user_user_id: Mapped[int] = mapped_column(primary_key=True)
    project_project_id: Mapped[int] = mapped_column(ForeignKey("project.project_id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_user_id", "role_id"],
            ["user.user_id", "user.role_role_id"],
        ),
    )

    user: Mapped["User"] = relationship(back_populates="project_memberships")
    project: Mapped["Project"] = relationship(back_populates="members")
