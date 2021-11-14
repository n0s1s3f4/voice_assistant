
import mysql.connector
import difflib

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
AIdict = []
def get_talkAI_database():
    cursor.execute("SELECT question FROM kira_talk_ai ORDER BY id") 
    questions = cursor.fetchall() # get questions
    cursor.execute("SELECT answer FROM kira_talk_ai ORDER BY id") 
    answers = cursor.fetchall() # get answers
    cursor.execute("SELECT COUNT(*) FROM kira_talk_ai")
    global count
    count = cursor.fetchall()[0][0]# get rows count
    i=0
    AIdictPartial=[0,'','']
    while i<count:
        AIdictPartial=[0,questions[i][0],answers[i][0]]
        AIdict.insert(i,AIdictPartial)
        i=i+1
    return AIdict  # В РЕЗУЛЬТАТЕ ПОЛУЧАЕМ МНОГОМЕРНЫЙ МАССИВ, ОДИН ЭЛЕМЕНТ ЭТО [0, ВОПРОС,ОТВЕТ]

def get_talkAI_answer(phrase):
    result_dict = AIdict
    i=0
    while i<count:
        result_dict[i][0]=difflib.SequenceMatcher(a=phrase,b=result_dict[i][1]).ratio()
        i = i+1
    print(result_dict)




get_talkAI_database()
get_talkAI_answer('отсоси мой член')
