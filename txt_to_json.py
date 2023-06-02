import json

dict_list=[]

with open('censor_dictionary.txt', encoding='utf-8') as f:
    for i in f:
        s=i.lower().split('\n')[0]
        if s!= '':
            dict_list.append(s)

with open('censor_dictionary_json.json','w', encoding='utf-8') as e:
    json.dump(dict_list, e)
