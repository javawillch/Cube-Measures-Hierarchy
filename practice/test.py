import json


json_data = open("Model.json", encoding = "utf-8").read()
data = json.loads(json_data)

#get all measures name(733rows)
all_measure_list = []
for table in data["model"]["tables"]:
    if "measures" in table:
        #measures is a list
        #print("tables : ", len(measures))
        measures = table["measures"]
        #check list length
        length = len(measures)
        for i in range(0, length):
            all_measure_list.append(measures[i]["name"])


#write file
file = open("data.txt", mode = "w", encoding = "utf-8")  

for measure in all_measure_list:
    file.write("(\'"+measure+"\')\n")
               
file.close()   