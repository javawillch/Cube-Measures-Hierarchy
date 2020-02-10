import json
from collections import defaultdict

#arrange to be delete scope
file_path = "inp_to_be_deleted_measures_list.txt"
to_be_delete_list = []
with open(file_path, mode = "r", encoding = "utf-8") as file:
    line_measure = file.readline()
    cnt = 1
    while line_measure:
        to_be_delete_list.append(line_measure.strip())
        #read next line
        line_measure = file.readline()

file.close()   

#get JSON data
json_data = open("inp_Model.bim", encoding = "utf-8").read()
data = json.loads(json_data)

del_num_dict = defaultdict(list)
table_length = len(data["model"]["tables"])

#check delete scope
for x in range(0, table_length):
    if "measures" in data["model"]["tables"][x]:
        #measures is a list
        measures = data["model"]["tables"][x]["measures"]
        #check list length
        measure_length = len(measures)
        for i in range(0, measure_length):

            for to_be_delete_measure in to_be_delete_list:

                if measures[i]["name"].upper() == to_be_delete_measure.upper():                    
                    del_num_dict[x].append(i)

#do delete (*delete sequence is important, DESC) 
for dic_key, dic_value in del_num_dict.items():
    table_num = dic_key
    #reverses the order of the list
    dic_value.sort()
    dic_value.reverse()

    dic_value_len = len(dic_value)
    for i in range(0, dic_value_len):
        measure_num = dic_value[i]
        del data['model']['tables'][table_num]['measures'][measure_num]


#write the modified result back
with open("opt_Model.bim", "w") as json_data:
    json.dump(data, json_data, indent = 2)
