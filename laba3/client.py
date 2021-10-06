import socket
import os
import sys
import xml.etree.ElementTree as ET
import json


def create_xml(**data):
    main_tag = ET.Element("Information")
    for key, val in data.items():
        title = ET.SubElement(main_tag, key)
        title.text = val
    doc = ET.tostring(main_tag, encoding="unicode")
    return doc


if __name__ == "__main__":
    print("Здравствуй, введи команду для работы с сервером!")
    print("<edb> - Изменить используемую БД!")
    print("<s> - Передать данные на сервер по пациенту!")
    # print("<g> - Получить информацию по пациенту!")
    print("<ex> - Выход из программы!")
    print()

    query_json = {"db": "nosql"} 
    # настройки подключения к серверу
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    while True:
        comand = str(input("Введите команду: "))
        if comand == 'ex':
            # sock.send(message.encode())
            print('Сессия завершена!')
            sock.close()
            sys.exit()
        elif comand == "edb":
            sock.send("edb".encode())
            print("Server: " + sock.recv(1024).decode())
        elif comand == "s":
            new_user = input("Новый пациент?: ")
            if new_user.lower() == "да":
                # id определится
                id_user = str(len(os.listdir(f"{os.getcwd()}{os.sep}Server_DB_nosql")) + 1)
                # Создается запись по пациенту
                fname = str(input("Введите имя пациента: "))
                mname = str(input("Введите отчество пациента: "))
                sname = str(input("Введите фамилию пациента: "))
                bdate = str(input("Введите дату рождения пациента: "))
                oms = str(input("Введите номер полиса пациента: "))
                xml = create_xml(ID=id_user, FName=fname, SName=sname, MName=mname, OMS=oms) 
                print("\n", xml, "\n", end="\n")
                # Отправим на сервер
                sock.send(xml.encode())
                # Вывод результата обработки сервером
                print("Server: " + sock.recv(1024).decode())
            else:
                id_user = input("Введите id пациента: ")
                tdate = input("Введите дату сдачи теста пациентом: ")
                ttype = input("Введите тип теста: ")
                taquan = input("Введите результат тестирования (количественный): ")
                taqual = input("Введите результат тестирования (качественный): ")
                lab = input("Введите название лаборатории: ")
                data_json = {
                            "ID": id_user,
                            "TDate": tdate,
                            "TType": ttype,
                            "TAccQuantitative": taquan,
                            "TAccQualitative": taqual,
                            "Lab": lab
                }
                print("\n", data_json, "\n", end="\n")
                # Отправим на сервер
                send_json = json.dumps(data_json)
                sock.send(send_json.encode())
                # Вывод результата обработки сервером
                print("Server: " + sock.recv(1024).decode())
        else:
            # Неверная команда!
            print("LOL!")
