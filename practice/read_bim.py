import json

#read file
json_data = open("Model.bim", encoding = "utf-8").read()
data = json.loads(json_data)

#warm up
"""
get all table names(43 rows)
"""
all_table_list = []
for table in data["model"]["tables"]:
    all_table_list.append(table["name"])

#get all measures name(733rows)
all_measure_list = []
for table in data["model"]["tables"]:
    if "measures" in table:
        #measures is a list
        measures = table["measures"]
        #check list length
        length = len(measures)
        for i in range(0, length):
            all_measure_list.append(measures[i]["name"])


#get all unhidden measures name(21 rows)
unhidden_measure_list = []
for table in data["model"]["tables"]:
    if "measures" in table:
        #measures is a list
        measures = table["measures"]
        #check list length
        length = len(measures)
        for i in range(0, length):
            #next line means current measure is show outside
            if "isHidden" not in measures[i]:  
                unhidden_measure_list.append(measures[i]["name"])


print("table count: ", len(all_table_list))
print("measure count: ", len(all_measure_list))
print("visiable meausre count: ", len(unhidden_measure_list))
#create a dic (measure, sub_measure)


###########################
#show hierarchy


###########################

#scope need to be deleted

#do delete in JSON

#write in JSON