import socket
import os
import sys
import json
import pyodbc
import math
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
            "db": "medicine",
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
                    day = random.randint(1, 30)
                    # ограничения для февраля, чтобы чуть чуть похоже было на правдободные данные
                    if month == 2 and day > 28:
                        day = 28
                    bdate = f"{year}-{month}-{day}"
                    oms = f"{random.randrange(1, 10 ** 16)}"
                    # Строка для добавления инфы по омс
                    print("1")
                    query_add_oms = f"INSERT INTO policy(num_oms) VALUES({oms});"
                    cursor_db.execute(query_add_oms)
                    print("2")
                    query_get_id_oms = f"SELECT LAST_INSERT_ID();"
                    cursor_db.execute(query_get_id_oms)
                    id_oms = cursor_db.fetchone()[0]
                    # Строку для добавления инфы по пациентам
                    print("3")
                    query_add_patient = f"INSERT INTO patient(fname, mname, sname, bdate, id_Policy) \
                                          VALUES('{f}', '{m}', '{s}', '{bdate}', {id_oms});"
                    cursor_db.execute(query_add_patient)
                    print("готово!")
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
            # будем генерировать за сентябрь
            month = 9
            year = 2021
            day = random.randint(1, 30)
            tdate = f"{year}-{month}-{day}"
            # Выполняем запрос и получаем созданный id результата теста
            query_add_res_test = f"INSERT INTO resulttest(taquan, taqual, tdate) VALUES({taquan}, '{taqual}', '{tdate}');"
            cursor_db.execute(query_add_res_test)
            query_get_id_res_test = "SELECT LAST_INSERT_ID();"
            cursor_db.execute(query_get_id_res_test)
            res_query_get_id_res_test = cursor_db.fetchone()[0]
            # Рандомно присваиваем организацию, которая делала тест
            id_organization = random.choice(res_query_get_id_organization)
            query_add_test_patient = f"INSERT INTO patienttest(id_Patient, id_TypeTest, id_ResultTest, id_Organization)"\
                                     f"VALUES({id_patient[0]}, " \
                                     f"{res_query_get_id_type_test}, " \
                                     f"{res_query_get_id_res_test}," \
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
    try:
        # Пишем Select запрос
        print("начало")
        print(f"'{query_data.fname=}', '{query_data.mname=}', '{query_data.sname=}', '{query_data.oms=}'")
        query_get_info_patient = f"SELECT p.fname, p.mname, p.sname, pol.num_oms, tt.name, " \
                                        f"rt.taquan, rt.taqual, rt.tdate, org.name " \
                                 f"FROM patient p " \
                                        f"JOIN policy pol ON p.id_Policy = pol.id_Policy " \
                                        f"JOIN patienttest pt ON pt.id_Patient = p.id_Patient " \
                                        f"JOIN typetest tt ON pt.id_TypeTest = tt.id_TypeTest " \
                                        f"JOIN resulttest rt ON pt.id_ResultTest = rt.id_ResultTest " \
                                        f"JOIN organization org ON pt.id_Organization = org.id_Organization " \
                                 f"WHERE p.fname = '{query_data.fname}' and p.mname = '{query_data.mname}' " \
                                        f"and p.sname = '{query_data.sname}' and pol.num_oms = '{query_data.oms}';"
        # Делаем запрос
        print("запрос")
        cursor_db.execute(query_get_info_patient)
        print("колонки:")
        cols = [column[0] for column in cursor_db.description]
        print(cols)
        print("ответ запроса:")
        res_query_get_info_patient = cursor_db.fetchall()
        print(res_query_get_info_patient)
    except pyodbc.DatabaseError as err:
        print("Неудача!")
        return f"Произошел конфуз с бд({err})"
    # обрабатываем запрос и возвращаем его пользователю
    # комит
    return {"head": cols, "response": res_query_get_info_patient}


def print_table(dt_js):
    cols = {
            "1": 20,
            }
    head = dt_js["head"]
    resp_table = []
    s_s = ["+"+"-"*cols["1"] for _ in range(len(head))]
    #print(*s_s, "+", sep="")
    resp_table.append("".join(s_s) + "+")

    row = ""
    for col_name in head:
        start = math.floor((cols["1"] - len(col_name)) / 2)
        end = math.ceil((cols["1"] - len(col_name)) / 2)
        row += "|" + f" " * start + f"{col_name}" + f" " * end
    row += "|"
    #print(row)
    resp_table.append(row)

    #print(*s_s, "+", sep="")
    resp_table.append("".join(s_s) + "+")

    for data in dt_js["response"]:
        row = ""
        for elem in data:
            if len(str(elem)) >= cols["1"]:
                elem = "%.6f" % elem
                start = math.floor((cols["1"] - len(str(elem))) / 2)
                end = math.ceil((cols["1"] - len(str(elem))) / 2)
                row += "|" + f" " * start + f"{elem}" + f" " * end
            else:
                start = math.floor((cols["1"] - len(str(elem))) / 2)
                end = math.ceil((cols["1"] - len(str(elem))) / 2)
                row += "|" + f" " * start + f"{elem}" + f" " * end
        row += "|"
        #print(row)
        resp_table.append(row)
        #print(*s_s, "+", sep="")
        resp_table.append("".join(s_s) + "+")

    return resp_table


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
                    conn.send("Генерация пациентов проведена успешно!".encode())
                else:
                    print("Генерация пациентов завершена с провалом!")
                    conn_db.rollback()
                    conn.send(res.encode())
            elif "gen_res" in data.decode():
                print("Функция gen_res")
                data = json.loads(data.decode())
                res = gen_res(cursor, data["type_test"])
                print(res)
                if res == True:
                    print("Генерация тестов проведена успешно!")
                    conn.send("Генерация тестов проведена успешно!".encode())
                else:
                    print("Генерация тестов завершена с провалом!")
                    conn.send(res.encode())
            elif "query_db" in data.decode():
                res = query_db(cursor, data)
                print(res)
                if isinstance(res, dict):
                    print("Запрос успешно выполнен!")
                    # Пока под вопросом
                    resp_table = {}
                    resp_table["table"] = print_table(res)
                    print(resp_table["table"])
                    conn.send(json.dumps(resp_table, default=str).encode())
                else:
                    print("Запрос провален!")
                    # Пока под вопросом
                    conn.send(res.encode())

    conn.close()
