from src.skill_matrix.database import engine, SessionLocal
from src.skill_matrix.models import Base
from src.skill_matrix import crud

#Удвление всех таблиц
def drop_all_tables():
    Base.metadata.drop_all(engine)
    print("Все таблицы удалены")


def main():
    drop_all_tables() 
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # Создание ролей
        employee_role = crud.read_role_by_name(session, "employee") or crud.create_role(session, "employee")
        manager_role = crud.read_role_by_name(session, "manager")  or crud.create_role(session, "manager")
        print("1. Роли:", [r.name for r in crud.read_all_roles(session)])

        # Регистрация пользователей
        manager = crud.create_user(session, "anna", "anna@example.com", "123", manager_role.role_id, "HR")
        employee = crud.create_user(session, "ivan", "ivan@example.com", "111", employee_role.role_id)
        print("2. Пользователи:", [(u.username, u.role.name) for u in crud.read_all_users(session)])

        # Создание навыков
        python_skill = crud.create_skill(session, "Python", "Language")
        sql_skill = crud.create_skill(session, "SQL", "Database")
        print("3. Навыки:", [s.name for s in crud.read_all_skills(session)])

        # Добавление навыков сотруднику
        crud.add_skill_to_user(session, employee.user_id, python_skill.skill_id, 3)
        crud.add_skill_to_user(session, employee.user_id, sql_skill.skill_id, 2)
        print("4. Навыки Ивана:", [(us.skill.name, us.level) for us in crud.read_user_skills(session, employee.user_id)])

        # Создание проекта менеджером
        project = crud.create_project(
            session, "ReDepict", "AI-сервис для начинающих художников", manager.user_id
        )
        print("5. Проекты:", [(p.title, p.manager.username) for p in crud.read_all_projects(session)])

        # Назначить  на проект
        crud.assign_user_to_project(session, employee.user_id, project.project_id)
        print("6. Участники проекта:", [u.username for u in crud.read_project_members(session, project.project_id)])

        # Поиск кандидатов по навыку
        candidates = crud.find_users_by_skill(session, "Python", min_level=2)
        print("7. Кандидаты с Python >= Middle:", [u.username for u in candidates])

        # Обновление профиля
        crud.update_user(session, employee.user_id, department="Backend")
        updated = crud.read_user(session, employee.user_id)
        print(f"8. Иван после обновления: department={updated.department}")

        # Удаление навыка
        crud.remove_skill_from_user(session, employee.user_id, sql_skill.skill_id)
        print("9. Навыки Ивана после удаления SQL:", [us.skill.name for us in crud.read_user_skills(session, employee.user_id)])


if __name__ == "__main__":
    main()