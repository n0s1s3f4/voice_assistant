import time
import difflib
import linecache
def talk(result):
    database = open("answer_database.txt", "r",encoding='utf-8')
    i=0
    seq_dict = {}
    sequence = ['','','']
    answer_dict = {}
    def similar(seq1,seq2):
        return difflib.SequenceMatcher(a=seq1,b=seq2).ratio()
    while i<8000:
        line = database.readline()
        if not line:
            break
        splitted = line.split('=')
        splitted[1] = splitted[1].replace("\n","")
        sequence[0] = splitted[0]
        sequence[1] = splitted[1]
        sequence[2] = i+1
        seq_dict[sequence[2]] = similar(result,sequence[0])
        answer_dict[sequence[2]] = splitted[1]
        i=i+1
       # print(sequence)
    #print(seq_dict)
    sorted_dict = sorted(seq_dict.items(), key=lambda x: x[1])
    resultat = sorted_dict[7999][0]
    answer = answer_dict.get(resultat)
    database.close()
    return str(answer)
    
if 1==1:
    print(talk("приветик парень"))

