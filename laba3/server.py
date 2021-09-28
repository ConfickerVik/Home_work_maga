import socket
import os
import xml
import pyodbc
import json
import xml.etree.ElementTree as ET
from jsonschema import validate


class Setting:
    def __init__(self):
        self.sett_sql_db = {
                            "host": "",
                            "user": "",
                            "password": "",
                            "db": ""
        }
        self.sett_nosql_db = {
                            "path_no_sql": f"{os.getcwd}{os.sep}Server_DB_nosql{os.sep}"
        }
        self.use_db = "nosql" # or sql
        self.sett_socket = {
                            "socket_host": 9090,
                            "socket_listen": 1
        }


def edb(sett):
    sett.use_db = "nosql" if sett.use_db != "sql" else "sql"
    return sett


def validate_xml(tree):
    val = []
    for elem in tree.iter():
        if elem.tag == "ID":
            val.append(True)
        elif elem.tag == "FName":
            val.append(True)
        elif elem.tag == "MName":
            val.append(True)
        elif elem.tag == "SName":
            val.append(True)
        elif elem.tag == "BDate":
            val.append(True)
        elif elem.tag == "OMS":
            val.append(True)
        else:
            val.append(False)
    if len(set(val)) > 1 and len(val) == 6:
        return False
    return True


def validate_json(json_data):
    schema = {
        "type": "object",
        "properties": {
            "ID": {
                "type": "string"
            },
            "TDate": {
                "type": "string"
            },
            "TType": {
                "type": "string",
                "enum": ["IgM", "IgG"]
            },
            "TAccQuantitative": {
                "type": "string"
            },
            "TAccQualitative": {
                "type": "string"
            },
            "Lab": {
                "type": "string"
            }
        }
    }
    try:
        validate(schema=schema, instance=json_data)
    except Exception as ex:
        return False
    return True


if __name__ == "__main__":
    settings = Setting()
    #db = DBConnect()
    #db.connect(settings)
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()

    print('connected:', addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        else:
            if data.decode() == "edb":
                settings = edb(settings)
                answer_server = f"Вы используете {settings.use_db} базу данных!"
                conn.send(answer_server.encode())
            try:
                data = json.loads(data.decode())
            except Exception as e:
                data = ET.fromstring(data.decode())

            if isinstance(data, xml.etree.ElementTree.Element):
                print(data)
                res_validate_xml = validate_xml(data)
                if res_validate_xml == False:
                    answer_server = "Ошибка заполнения, валидация XML не пройдена!"
                else:
                    answer_server = "Валидация пройдена успешно!"
                conn.send(answer_server.encode())
                # if settings.use_db == "nosql":
                #    # Логика работы с нереляционной бд
                #    pass
                # else:
                #     # Логика работы с реляционной бд
                #     pass
            if isinstance(data, dict):
                print(data)
                res_validate_json = validate_json(data)
                if res_validate_json == False:
                    answer_server = "Ошибка заполнения, валидация JSON не пройдена!"
                else:
                    answer_server = "Валидация пройдена успешно!"
                conn.send(answer_server.encode())
                # if settings.use_db == "nosql":
                #    # Логика работы с нереляционной бд
                #    pass
                # else:
                #     # Логика работы с реляционной бд
                #     pass

    conn.close()
