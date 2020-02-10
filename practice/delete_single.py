import json

#get JSON data
json_data = open("Model_test.json").read()
data = json.loads(json_data)


all_measure_list = []
del_num_dict = dict()
table_length = len(data["model"]["tables"])

for x in range(0, table_length):
    if "measures" in data["model"]["tables"][x]:
        #measures is a list
        measures = data["model"]["tables"][x]["measures"]
        #check list length
        measure_length = len(measures)
        for i in range(0, measure_length):
            all_measure_list.append(measures[i]["name"])
            if measures[i]["name"] == 'SR - Depl6oyed SB Active Customer Count_Org':
                #print("total len: ", measure_length, "num: ", i )
                del_num_dict[x] = i
                #del data['model']['tables']['measures'][i]
                #del measures[i]

for dic in del_num_dict:
    table_num = dic
    measure_num = del_num_dict.get(dic)
    #print(data['model']['tables'][table_num]['measures'][measure_num])
    del data['model']['tables'][table_num]['measures'][measure_num]


#write the modified result back
with open("new_Model_test.json", "w") as json_data:
    json.dump(data, json_data, indent = 2)
