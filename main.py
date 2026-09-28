from src.skill_matrix.database import engine, SessionLocal
from src.skill_matrix.models import Base
from src.skill_matrix import crud


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # Создание ролей
        employee_role = crud.read_role_by_name(session, "employee") or crud.create_role(session, "employee")
        manager_role = crud.read_role_by_name(session, "manager")  or crud.create_role(session, "manager")

        # Регистрация пользователей
        manager = crud.create_user(session, "anna", "anna@example.com", "123", manager_role.role_id, "HR")
        employee = crud.create_user(session, "ivan", "ivan@example.com", "111", employee_role.role_id)

        # Создание навыков
        python_skill = crud.create_skill(session, "Python", "Language")
        sql_skill = crud.create_skill(session, "SQL", "Database")

        # Добавление навыков сотруднику
        crud.add_skill_to_user(session, employee.user_id, python_skill.skill_id, 3)
        crud.add_skill_to_user(session, employee.user_id, sql_skill.skill_id, 2)
        print("Навыки Ивана:", [(us.skill.name, us.level)for us in crud.read_user_skills(session, employee.user_id)])

        # Создание проекта менеджером
        project = crud.create_project(
            session, "ReDepict", "AI-сервис для начинающих художников", manager.user_id
        )

        # Назначить  на проект
        crud.assign_user_to_project(session, employee.user_id, project.project_id)

        # Поиск кандидатов по навыку
        candidates = crud.find_users_by_skill(session, "Python", min_level=2)
        print("Кандидаты с Python >= Middle:", [u.username for u in candidates])

        # Обновление профиля
        crud.update_user(session, employee.user_id, department="Backend")

        # Удаление навыка
        crud.remove_skill_from_user(session, employee.user_id, sql_skill.skill_id)


if __name__ == "__main__":
    main()