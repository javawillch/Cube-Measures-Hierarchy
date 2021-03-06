import json
from collections import defaultdict
"""
#save_01
\n mean 換行

file = open("data.txt", mode = "w", encoding = "utf-8")  
file.write("Hello\n 泥好 \nFile")                  
file.close()

#save_02
#這種寫法不用close
with open("data.txt", mode = "w", encoding = "utf-8") as file:
    file.write("Hello\n 泥好 \nFile\n020202")                   

#read_01
with open("data.json", mode = "r", encoding = "utf-8") as file:
    json_data = file.read()


#print(type(data["model"]))  # <class 'dict'>
#print("measure", data["measures"])
"""
#read_02
json_data = open("Model.bim", encoding = "utf-8").read()
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

#transformat to upper case in order to compare later
all_measure_list_upper_case = []
for measure in all_measure_list:
    all_measure_list_upper_case.append(str(measure).upper())

#get all unhidden measures name(21rows)
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




measure_with_submeasure_dic = defaultdict(list) #571(rows) --> #576(rows)
for table in data["model"]["tables"]:
    if "measures" in table:
        #measures is a list
        measures = table["measures"]
        #check list length
        length = len(measures)
        for i in range(0, length):

            measure_name = str(measures[i]["name"])
            #get expression like [ ......[].....[]....]
            expres = str(measures[i]["expression"])
            if expres.count("[") > 1:
                #strip first and end []
                expres = expres[1:len(expres)-1]


            #if measure_name.upper() == "Partner Retention Rate (YoY)_Org".upper():
            #check how many possible measures
            while expres.find("[") >= 0 and expres.find("]") >= 0:
                start_num = expres.find("[")+1
                end_num = expres.find("]")
                possible_measure = expres[start_num: end_num]                    
                #if match, add dic
                if possible_measure.upper() in all_measure_list_upper_case:
                    if possible_measure == "Lost Customer Count_All" and measure_name == 'Lost Customer Count Control_SP_All':
                        #print(measure_name, possible_measure)  
                        print("measure_name: ", measure_name)
                        print("measure_name_get_value: ",measure_with_submeasure_dic.get(measure_name))
                        print("possible_measure: ",possible_measure)
                    #add dic
                    sub_measure_group_up = [ x.upper() for x in measure_with_submeasure_dic[measure_name] ]
                    #sub_measure_group = measure_with_submeasure_dic[measure_name]
                    if sub_measure_group_up == None:
                        measure_with_submeasure_dic[measure_name].append(possible_measure)
                    else:
                        #if already has same value, then skip
                        if possible_measure.upper() not in sub_measure_group_up:
                            measure_with_submeasure_dic[measure_name].append(possible_measure)
                    ###print("measure: ", measure_name, " sub measure: ", measure_with_submeasure_dic.get(measure_name))

                #curtail string
                expres = expres[end_num+1:len(expres)]


               
#for x in measure_with_submeasure_dic:
    #write dictnary 
    #file.write("["+ x +"] : ["+ measure_with_submeasure_dic.get(x)+ "]\n")
    #print("[",x,"] : [", measure_with_submeasure_dic.get(x), "]")




#print(len(measure_with_submeasure_dic))


measure_with_submeasure_list = [] #1607(rows)   --> 972(rows)  --> 1652(rows)  --> 982(rows)
for x in measure_with_submeasure_dic:
    value_list = measure_with_submeasure_dic.get(x)
    for i in value_list:
        measure_with_submeasure_list.append([x, i])

measure_with_submeasure_list.sort()         

file = open("LoadData.sql", mode = "w", encoding = "utf-8")  

for x in measure_with_submeasure_list:
    print("(\'"+x[0]+"\',\'"+x[1]+"\')")
    file.write("INSERT INTO [DQ].[dbo].[Cube_Measure_Hierarchy] ([Measure], [Sub_Measure]) VALUES (\'"+x[0]+"\',\'"+x[1]+"\')\n")

print(len(measure_with_submeasure_list))       

file.close()



"""
json資料讀法
data["measures"]
data.items()
"""


