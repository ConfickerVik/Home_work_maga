import json
import socket
import os
import sys

if __name__ == "__main__":
    print("Здравствуй, введи команду для работы с сервером!")
    print("<genuser> - Сгенерировать пользователей и их омс!")
    print("<genres> - Сгенерировать результаты тестов!")
    print("<query> - Отправить запрос в бд!")
    print("<ex> - Выход из программы!")

    # настройки подключения к серверу
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    while True:
        query_json = {}
        comand = str(input("\nВведите команду: "))
        if comand == 'ex':
            # sock.send(message.encode())
            print('Сессия завершена!')
            sock.close()
            sys.exit()
        elif comand == "genuser":
            fname = [str(input(f"Введите {x + 1}-ое имя: ")) for x in range(3)]
            mname = [str(input(f"Введите {x + 1}-ую отчество: ")) for x in range(3)]
            sname = [str(input(f"Введите {x + 1}-ое фамилию: ")) for x in range(3)]
            query_json["comand"] = "gen_user"
            query_json["data"] = [fname, mname, sname]
            # Отправляем на серв, там сгенерируем номера омс и даты рождения
            sock.send(json.dumps(query_json).encode())
            # Печатаем ответ сервера
            print(sock.recv(1024).decode())
        elif comand == "genres":
            query_json["comand"] = "gen_res"
            query_json["type_test"] = "IgM"
            # Отправляем на серв, там сгенерируем номера омс и даты рождения
            sock.send(json.dumps(query_json).encode())
            # Печатаем ответ сервера
            print(sock.recv(1024).decode())
        elif comand == "query":
            print("Вы попали в мир запросов) Вам необходимо ввести некоторые данные: ")
            fname = str(input("Введите имя пациента: "))
            mname = str(input("Введите отчество пациента: "))
            sname = str(input("Введите фамилию пациента: "))
            oms = input("Введите номер омс пациента: ")
            query_json["comand"] = "query_db"
            query_json["fname"] = fname
            query_json["mname"] = mname
            query_json["sname"] = sname
            query_json["oms"] = oms
            # Отправляем на серв, там сгенерируем номера омс и даты рождения
            sock.send(json.dumps(query_json).encode())
            # Печатаем ответ сервера
            print("\nРезультат запроса: ")
            response = sock.recv(2048).decode()
            resp_json = json.loads(response)
            for row in resp_json["table"]:
                print(row)
        else:
            # sock.send(message.encode())
            # Вывод результата обработки сервером
            # print(sock.recv(1024).decode())
            print("LOL!")