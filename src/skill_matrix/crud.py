from sqlalchemy import select
from sqlalchemy.orm import Session

from src.skill_matrix.models import (Role, User, Skill, Project, UserSkill, ProjectMember)

#Удвление всех таблиц

def drop_all_tables():
    Base.metadata.drop_all(engine)
    print("Все таблицы удалены")

# ROLE

def create_role(session: Session, name: str) -> Role:
    role = Role(name=name)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

def read_role(session: Session, role_id: int) -> Role | None:
    return session.get(Role, role_id)

def read_role_by_name(session: Session, name: str) -> Role | None:
    return session.scalar(select(Role).where(Role.name == name))

def read_all_roles(session: Session) -> list[Role]:
    return list(session.scalars(select(Role)))

def update_role(session: Session, role_id: int, name: str) -> Role | None:
    role = session.get(Role, role_id)
    if role:
        role.name = name
        session.commit()
        session.refresh(role)
    return role

def delete_role(session: Session, role_id: int) -> bool:
    role = session.get(Role, role_id)
    if role:
        session.delete(role)
        session.commit()
        return True
    return False


# USER

def create_user(session: Session, username: str, email: str, password: str, role_id: int, department: str | None = None) -> User:
    user = User(
        username=username,
        email=email,
        password=password,
        role_id=role_id,
        department=department,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def read_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def read_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))

def read_all_users(session: Session) -> list[User]:
    return list(session.scalars(select(User)))

def update_user(session: Session, user_id: int, username: str | None = None, email: str | None = None, department: str | None = None) -> User | None:
    user = session.get(User, user_id)
    if user:
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if department is not None:
            user.department = department
        session.commit()
        session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

def find_users_by_skill(session: Session, skill_name: str, min_level: int = 1) -> list[User]:
    """Найти пользователей с указанным навыком и уровнем не ниже min_level"""
    stmt = (
        select(User)
        .join(UserSkill, User.user_id == UserSkill.user_id)
        .join(Skill, UserSkill.skill_id == Skill.skill_id)
        .where(Skill.name == skill_name)
        .where(UserSkill.level >= min_level)
    )
    return list(session.scalars(stmt))

def read_user_skills(session: Session, user_id: int) -> list[UserSkill]:
    return list(session.scalars(select(UserSkill).where(UserSkill.user_id == user_id)))



# SKILL

def create_skill(session: Session, name: str, category: str | None = None) -> Skill:
    skill = Skill(name=name, category=category)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

def read_skill(session: Session, skill_id: int) -> Skill | None:
    return session.get(Skill, skill_id)

def read_skill_by_name(session: Session, name: str) -> Skill | None:
    return session.scalar(select(Skill).where(Skill.name == name))


def read_all_skills(session: Session) -> list[Skill]:
    return list(session.scalars(select(Skill)))

def update_skill(session: Session, skill_id: int, name: str | None = None, category: str | None = None) -> Skill | None:
    skill = session.get(Skill, skill_id)
    if skill:
        if name is not None:
            skill.name = name
        if category is not None:
            skill.category = category
        session.commit()
        session.refresh(skill)
    return skill

def delete_skill(session: Session, skill_id: int) -> bool:
    skill = session.get(Skill, skill_id)
    if skill:
        session.delete(skill)
        session.commit()
        return True
    return False

def add_skill_to_user(session: Session, user_id: int, skill_id: int, level: int) -> UserSkill:
    us = UserSkill(user_id=user_id, skill_id=skill_id, level=level)
    session.add(us)
    session.commit()
    return 

def remove_skill_from_user(session: Session, user_id: int, skill_id: int) -> bool:
    us = session.get(UserSkill, (user_id, skill_id))
    if us:
        session.delete(us)
        session.commit()
        return True
    return False


# PROJECT

def create_project(session: Session, title: str, description: str | None, manager_id: int) -> Project:
    project = Project(
        title=title,
        description=description,
        manager_id=manager_id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def read_project(session: Session, project_id: int) -> Project | None:
    return session.get(Project, project_id)

def read_all_projects(session: Session) -> list[Project]:
    return list(session.scalars(select(Project)))

def update_project(session: Session, project_id: int, title: str | None = None, description: str | None = None) -> Project | None:
    project = session.get(Project, project_id)
    if project:
        if title is not None:
            project.title = title
        if description is not None:
            project.description = description
        session.commit()
        session.refresh(project)
    return project

def delete_project(session: Session, project_id: int) -> bool:
    project = session.get(Project, project_id)
    if project:
        session.delete(project)
        session.commit()
        return True
    return False

def assign_user_to_project(session: Session, user_id: int, project_id: int) -> ProjectMember:
    pm = ProjectMember(user_id=user_id, project_id=project_id)
    session.add(pm)
    session.commit()
    return pm

def read_project_members(session: Session, project_id: int) -> list[User]:
    """Cисок участников проекта"""
    project = session.get(Project, project_id)
    if not project:
        return []
    return [pm.user for pm in project.members]