from logging import log
from os import sep
from peewee import PeeweeException
from _database import *

# from utils import _AutoInit


class DatabaseManager:
    def __init__(self) -> None:
        self.driver = database

    def sign_in(self, login: str, password: str) -> bool or Exception:
        cursor = database.execute_sql(
            f"SELECT * FROM larionova.user WHERE larionova.user.login='{login}' AND larionova.user.password='{password}';"
        )
        print(
            f"SELECT * FROM larionova.user WHERE larionova.user.login='{login}' AND larionova.user.password='{password}';"
        )

        user = cursor.fetchone()

        if not user:
            return False

        return user

    def sign_up(self, login: str, password: str) -> bool or Exception:
        try:
            database.execute_sql(
                f"INSERT INTO larionova.user(login, password, role) VALUES('{login}', '{password}', 'Заказчик');"
            )
            return True
        except PeeweeException:
            return False
        except:
            return None

    def get_all_fittings(self) -> list:
        cursor = database.execute_sql(
            f"SELECT vendor_code, name, unit, amount, provider_id, accessories_type, purchase_price, weight FROM fittings;"
        )

        fittings = list()

        for row in cursor.fetchall():
            fittings.append(row)

        return fittings
        

#     def get_subjects_for_professor(self, professor_id: int) -> list:
#         cursor = database.execute_sql(
#             f"SELECT name FROM subjects WHERE professor_id={professor_id};"
#         )

#         subjects = list()

#         for row in cursor.fetchall():
#             subjects.append(_Subject(professor_id=professor_id, name=row[0],))

#         return subjects

#     def get_all_professors(self) -> list:
#         cursor = database.execute_sql(
#             f"SELECT id, first_name, last_name, patronymic FROM professors;"
#         )

#         professors = list()

#         for row in cursor.fetchall():
#             professors.append(
#                 _Professor(
#                     id=row[0], first_name=row[1], last_name=row[2], patronymic=row[3],
#                 )
#             )

#         return professors

#     def get_all_difficulties(self) -> list:
#         cursor = database.execute_sql(f"SELECT complexity FROM complexity;")

#         difficulties = list()

#         for row in cursor.fetchall():
#             difficulties.append(_Difficulty(complexity=row[0],))

#         return difficulties

#     # def get_tasks(complexity) -> dict:
#     #     cursor = database.execute_sql(f"SELECT complexity from complexity;")

#     #     tasks = list()

#     #     for row in cursor.fetchall():
#     #         difficulties.append(_Difficulty(complexity=row[0],))

#     #     return difficulties

#     def get_count_tasks(
#         self, comlexity_list, subject_professor_id, subject_name
#     ) -> list:
#         comlexity_list_str = "".join(
#             [f"'{comlexity}'," for comlexity in comlexity_list]
#         )[:-1]
#         cursor = database.execute_sql(
#             f"SELECT tasks.complexity_id, count(tasks.text) FROM tasks WHERE tasks.complexity_id IN ({comlexity_list_str}) AND tasks.subject_professor_id = {subject_professor_id} AND subject_name = '{subject_name}' GROUP BY tasks.complexity_id;"
#         )

#         tasks = list()

#         for row in cursor.fetchall():
#             tasks.append(_TaskCount(comlexity=row[0], count=row[1]))
#             comlexity_list.remove(row[0])

#         for comlexity in comlexity_list:
#             tasks.append(_TaskCount(comlexity=comlexity, count=0))

#         return tasks

#     def get_tasks(self, complexity, subject_professor_id, subject_name, limit):
#         cursor = database.execute_sql(
#             f"""SELECT tasks.text FROM tasks
# WHERE tasks.complexity_id = '{complexity}'
# AND tasks.subject_professor_id = {subject_professor_id}
# AND tasks.subject_name = '{subject_name}'
# LIMIT {limit};"""
#         )

#         tasks = list()

#         for row in cursor.fetchall():
#             tasks.append(row[0].strip())

#         return tasks

