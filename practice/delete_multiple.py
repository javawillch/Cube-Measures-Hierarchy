import json
from collections import defaultdict

#get JSON data
json_data = open("Model_test.json").read()
data = json.loads(json_data)

to_be_delete_list = []
del_num_dict = defaultdict(list)
table_length = len(data["model"]["tables"])

#arrange to be delete scope
to_be_delete_list.append('New Logo Customer Count_Org')
to_be_delete_list.append('New Logo Customer Count Control_Org')
#to_be_delete_list.append('Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed SB Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed SB_L0 Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed SB_L1 Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed SB_L2 Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed ENT Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed ENT_L0 Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed ENT_L1 Active Customer Count_Org')
to_be_delete_list.append('SR - Deployed ENT_L2 Active Customer Count_Org')


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



    #measure_num = del_num_dict.get(dic_key)
    #print(dic_value)
    #print(str(table_num) + ' , ' + str(measure_num) + ' \n')
#    for measure_num in dic_value:
#        del data['model']['tables'][table_num]['measures'][measure_num]
    #print(data['model']['tables'][table_num]['measures'][measure_num])
    #del data['model']['tables'][table_num]['measures'][measure_num]


#write the modified result back
with open("new_Model_test.json", "w") as json_data:
    json.dump(data, json_data, indent = 2)
