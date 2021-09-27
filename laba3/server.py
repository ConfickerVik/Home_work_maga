import socket
import os
import sys
import pyodbc


class DBConnect:
	def connect(self, settings):
		connection = pymysql.connect(host = settings.sett_sql_db["host"],
			user = settings.sett_sql_db["user"],
			password = settings.sett_sql_db["password"],
			db = settings.sett_sql_db["db"],
			cursorclass = pymysql.cursors.DictCursor)
		cursor = connection.cursor()
		return cursor

	def query(self, cursor, querydb):
		cursor.execute(querydb)
		resQuary = cursor.fetchall()
		return resQuary


class Setting:
    def __init__(self):
        self.sett_sql_db = {
                            "host": ""
                            "user": ""
                            "password": ""
                            "db": ""
        }
        self.sett_nosql_db = {
                            "path_no_sql": f"{os.getcwd}{os.sep}Server_DB_nosql{os.sep}"
        }
        self.use_db = "nosql" # or sql
        self.sett_socket = {
                            "socket_host" = 1111
                            "socket_listen" = 2
        }
        
def edb(sett):
    sett.use_db = "nosql" if sett.use_db != "sql" else "sql"
    return sett

def s():
    pass

def g():
    pass


if __name__ == "__main__":
    settings = Setting()
    db = DBConnect()
    db.connect(settings)
    # sock = socket.socket()
    # sock.bind(('', 9090))
    # sock.listen(10)
    # conn, addr = sock.accept()

    # print('connected:', addr)

    dict_comand = {
        "edb":edb,
        "s":s,
        "g":g
    }

    while True:
        # data = conn.recv(1024)
        if not data:
            break
        else:
            # sonnet = getSonnet()
            # conn.send(sonnet.encode())
            if settings.use_db == "nosql":
                # Логика работы с нереляционной бд
                pass
            else:
                # Логика работы с реляционной бд
                pass

    # conn.close()
