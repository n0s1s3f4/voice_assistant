import os
import mysql.connector
database = open("answer_database.txt", "r",encoding='utf-8')


def create_connection(host_name, user_name, user_password,db_name,db_port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port = db_port
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("localhost", "root", "123098","kira_db","3306")
cursor = connection.cursor()

def main():
    print("Количество строк в импортируемом файле?")
    lines_count = int(input())
    i=1
    while i<lines_count:
            line = database.readline()
            if not line:
                break
            splitted = line.split('=')
            splitted[1] = splitted[1].replace("\n","")
            print(splitted)
            query = "insert into kira_talk_ai(question,answer) values(%s, %s)" 
            args = (splitted[0], splitted[1])
            cursor.execute(query,args)
            connection.commit() 
            i=i+1
    connection.close()

if 1==1:
    main()