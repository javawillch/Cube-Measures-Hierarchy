import json
from collections import defaultdict


def main():

    all_measure_list = []
    all_measure_list_upper_case = []
    visible_measure_list = []

    #read
    json_data = open("inp_Model.bim", encoding = "utf-8").read()
    data = json.loads(json_data)

    write_all_measures(
        json_data = data,
        opt_list = all_measure_list
    )
    transformat_to_upper_case(
        ipt_list = all_measure_list, 
        opt_list = all_measure_list_upper_case
    )
    write_visible_measures(
        json_data = data,
        opt_list = visible_measure_list
    )
    write_measure_hierarchy(
        json_data = data,
        all_measure_list_upper_case = all_measure_list_upper_case
    )


def write_measure_hierarchy(json_data, all_measure_list_upper_case):
    """
    1.parsing json into dict first
    2.transformat from dict to list
    3.write load data file
    iuput:  json_data, list for compare purpose 
    """    
    measure_with_submeasure_dic = defaultdict(list) #571(rows) --> #576(rows)
    for table in json_data["model"]["tables"]:
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
                        #if possible_measure == "Lost Customer Count_All" and measure_name == 'Lost Customer Count Control_SP_All':
                            #print(measure_name, possible_measure)  
                            #print("measure_name: ", measure_name)
                            #print("measure_name_get_value: ",measure_with_submeasure_dic.get(measure_name))
                            #print("possible_measure: ",possible_measure)
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
     
    measure_with_submeasure_list = [] #982(rows)
    for x in measure_with_submeasure_dic:
        value_list = measure_with_submeasure_dic.get(x)
        for i in value_list:
            measure_with_submeasure_list.append([x, i])

    measure_with_submeasure_list.sort()         

    file = open("opt_03_LoadData_Measure_Hierarchy.sql", mode = "w", encoding = "utf-8")  
    file.write("USE [DQ]\nGO\n")

    for x in measure_with_submeasure_list:
        file.write("INSERT INTO [DQ].[dbo].[Cube_Measure_Hierarchy] ([Measure], [Sub_Measure]) VALUES (\'"+x[0]+"\',\'"+x[1]+"\')\n")

    file.close()


def write_visible_measures(json_data, opt_list):
    #get all visible measures name(21rows)
    for table in json_data["model"]["tables"]:
        if "measures" in table:
            #measures is a list
            measures = table["measures"]
            #check list length
            length = len(measures)
            for i in range(0, length):
                #next line means current measure is show outside
                if "isHidden" not in measures[i]:  
                    opt_list.append(measures[i]["name"])

    #write load data for [Cube_Unhidden_Measure]
    file = open("opt_02_LoadData_All_Visible_Measures.sql", mode = "w", encoding = "utf-8")  
    file.write("USE [DQ]\nGO\n")

    for x in opt_list:
        file.write("INSERT INTO [DQ].[dbo].[Cube_Unhidden_Measure]([Measure]) VALUES (\'"+x+"\')\n")    

    file.close()
    return opt_list


def transformat_to_upper_case(ipt_list, opt_list):
    """
    transformat the value of list to upper case in order to compare purpose
    """
    for measure in ipt_list:
        opt_list.append(str(measure).upper())


def write_all_measures(json_data, opt_list):
    """
    1.read the json_data, and then add to list
    2.extract all measures name, and write into file 
    iuput: list, json_data 
    output: list, file
    """
    #get all measures name(733rows)
    for table in json_data["model"]["tables"]:
        if "measures" in table:
            #measures is a list
            #print("tables : ", len(measures))
            measures = table["measures"]
            #check list length
            length = len(measures)
            for i in range(0, length):
                opt_list.append(measures[i]["name"])

    #write load data for [Cube_All_Measure]
    file = open("opt_01_LoadData_All_Measures.sql", mode = "w", encoding = "utf-8")  
    file.write("USE [DQ]\nGO\n")

    for x in opt_list:
        file.write("INSERT INTO [DQ].[dbo].[Cube_All_Measure] ([Measure]) VALUES (\'"+x+"\')\n")    

    file.close()

    return opt_list


if __name__ == '__main__':
    main()