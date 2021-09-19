commands = [
['погода на улице','погода','погодой','улице','за','окном'],

['погода дома','комнате','температура','влажность','влажностью','температурой', 'в', 'дома','погода','доме'],

['включение лампы','включи','свет','посвети','мне'],

['выключение лампы','выключи','свет','хватит','светить']
 ]

result = ['свет','выключи']




command_dict = {}
i = 0
while i<len(commands):
    command_dict[commands[i][0]] = len(list(set(result) & set(commands[i])))
    i = i + 1
    print(command_dict)
print(command_dict)
sorted_command_dict = {}
sorted_command_keys = sorted(command_dict, key=command_dict.get, reverse=True) 
print(sorted_command_keys)
for w in sorted_command_keys:
    sorted_command_dict[w] = command_dict[w]

print(sorted_command_dict)
final_command = str(list(sorted_command_dict.keys())[0])
print('Наибольшее совпадение ' + final_command)