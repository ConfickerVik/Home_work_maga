import socket
import os
import sys
import json
import pyodbc
# import uuid
from pydantic import BaseModel, ValidationError
import random


class DBConnect:
    def __init__(self, param):
        self.user = param["user"]
        self.password = param["password"]
        self.server = param["server"]
        self.database = param["db"]
        self.driver = param["driver"]

    def connect(self):
        # Создаём строку подключения к бд
        odbc_conn_str = f'DRIVER={self.driver};\
                        SERVER = {self.server}; \
                        DATABASE = {self.database}; \
                        UID = {self.user}; \
                        PWD = {self.password}'
        # Подключаемся к бд
        conn = pyodbc.connect(odbc_conn_str)
        cursor = conn.cursor()
        print("Установлено соединение!")
        return conn, cursor


# Лучше черпать такие данные из os.environ, но для лабы так сделаю
class Setting:
    def __init__(self):
        self.sett_sql_db = {
            "server": "127.0.0.1",
            "user": "root",
            "password": "VPuRS*lodx854321",
            "db": "sys",
            "driver": "MySQL ODBC 5.3 ANSI Driver"
        }
        self.sett_socket = {
            "socket_host": 9090,
            "socket_listen": 1
        }


# Для валидации данных генерации пациентов
class User(BaseModel):
    comand: str
    data: list[list]


# Для валидации данных по запросу
class Query(BaseModel):
    comand: str
    fname: str
    mname: str
    sname: str
    oms: int


# генерация пациентов
def gen_user(cursor_db, input_json):
    # Попытка валидации
    try:
        user_data = User.parse_raw(input_json)
    except ValidationError as e:
        print(e.json())
        return "Введены некорректные данные для генерации пользователей!"
    # Логика работы с данными тут
    try:
        for f in user_data.data[0]:
            for m in user_data.data[1]:
                for s in user_data.data[2]:
                    month = random.randint(1, 12)
                    year = random.randint(1960, 2002)
                    day = random.randint(1, 31)
                    # ограничения для февраля, чтобы чуть чуть похоже было на правдободные данные
                    if month == 2 and day > 28:
                        day = 28
                    bdate = f"{year}-{month}-{day}"
                    oms = f"{random.randrange(1, 10 ** 16)}"
                    # Строка для добавления инфы по омс
                    query_add_oms = f"INSERT INTO policy(num_oms) VALUES({oms});"
                    cursor_db.execute(query_add_oms)
                    query_get_id_oms = f"SELECT MAX(id_Policy) FROM policy;"
                    cursor_db.execute(query_get_id_oms)
                    id_oms = cursor_db.fetchone()[0]
                    # Строку для добавления инфы по пациентам
                    query_add_patient = f"INSERT INTO patient(fname, mname, sname, bdate, id_policy) \
                                          VALUES({f}, {m}, {s}, {bdate}, {id_oms});"
                    cursor_db.execute(query_add_patient)
    except pyodbc.DatabaseError as err:
        print("Неудача!")
        return f"Произошел конфуз с бд({err})"
    # Комит изменений
    cursor_db.commit()
    return True


def gen_res(cursor_db, type_test):
    # Логика работы тут
    try:
        # все id пациентов
        query_get_all_id = "SELECT id_Patient FROM patient;"
        cursor_db.execute(query_get_all_id)
        res_query_get_all_id = cursor.fetchall()

        # Получаем id необходимого теста
        query_get_id_type_test = f"SELECT id_TypeTest FROM typetest WHERE name = '{type_test}';"
        cursor_db.execute(query_get_id_type_test)
        res_query_get_id_type_test = cursor_db.fetchone()[0]

        # Получаем id организаций
        query_get_id_organization = "SELECT id_Organization FROM organization;"
        cursor_db.execute(query_get_id_organization)
        res_query_get_id_organization = cursor_db.fetchall()

        # генерируем количественный и качественный результат
        for id_patient in res_query_get_all_id:
            taquan = random.uniform(0, 3)
            taqual = "Положительный" if taquan >= 1 else "Отрицательный"
            # Выполняем запрос и получаем созданный id результата теста
            query_add_res_test = f"INSERT INTO resulttest(taquan, taqual) VALUES({taquan}, {taqual});\
                                   SELECT LAST_INSERT_ID();"
            cursor_db.execute(query_add_res_test)
            res_query_add_res_test = cursor_db.fetchone()[0]
            # Рандомно присваиваем организацию, которая делала тест
            id_organization = random.choice(res_query_get_id_organization)
            query_add_test_patient = f"INSERT INTO patienttest(id_Patient, id_TypeTest, id_ResultTest, id_Organization)"\
                                     f"VALUES({id_patient[0]}, " \
                                     f"{res_query_get_id_type_test}, " \
                                     f"{res_query_add_res_test}," \
                                     f"{id_organization[0]});"
            cursor_db.execute(query_add_test_patient)

    except pyodbc.DatabaseError as err:
        print("Неудача!")
        return f"Произошел конфуз с бд({err})"
    # Комит изменений
    cursor_db.commit()
    return True


def query_db(cursor_db, input_json):
    try:
        query_data = Query.parse_raw(input_json)
    except ValidationError as e:
        print(e.json())
        return "Введены некорректные данные для исполнения запроса в БД!"
    # Логика работы тут
    # Пишем Select запрос
    # query_get = ""
    # Парсим данные, которые пришли
    # Делаем запрос
    # обрабатываем запрос и возвращаем его пользователю
    # комит
    return True


if __name__ == "__main__":
    settings = Setting()
    db = DBConnect(settings.sett_sql_db)
    conn_db, cursor = db.connect()
    sock = socket.socket()
    sock.bind(('', settings.sett_socket["socket_host"]))
    sock.listen(settings.sett_socket["socket_listen"])
    conn, addr = sock.accept()

    print('connected:', addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        else:
            # try:
            #     data = json.loads(data.decode())
            #     print(data)
            # except Exception as e:
            #     sock.send("Неудачная попытка выполнить команду".encode())
            if "gen_user" in data.decode():
                print("Функция gen_user")
                res = gen_user(cursor, data)
                print(res)
                if res == True:
                    print("Генерация пациентов проведена успешно!")
                    sock.send("Генерация пациентов проведена успешно!".encode())
                else:
                    print("Генерация пациентов завершена с провалом!")
                    conn_db.rollback()
                    sock.send(res.encode())
            elif "gen_res" in data.decode():
                print("Функция gen_res")
                data = json.loads(data.decode())
                res = gen_res(cursor, data["type_test"])
                print(res)
                if res == True:
                    print("Генерация тестов проведена успешно!")
                    sock.send("Генерация тестов проведена успешно!".encode())
                else:
                    print("Генерация тестов завершена с провалом!")
                    sock.send(res.encode())
            elif "query_db" in data.decode():
                res = query_db(cursor, data)
                print(res)
                if res == True:
                    print()
                    # Пока под вопросом
                    sock.send("".encode())
                else:
                    print()
                    # Пока под вопросом
                    sock.send(res.encode())

    conn.close()
