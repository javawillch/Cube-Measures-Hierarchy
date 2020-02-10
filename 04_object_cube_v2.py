import json
from collections import defaultdict

class Cube:

    cube_count = 0

    def __init__(self, name, file_name):
        super().__init__()
        self.name = name
        self.file_name = file_name
        Cube.cube_count += 1

    @property
    def bim(self):
        data_str = open(self.file_name, encoding="utf-8").read()        
        return json.loads(data_str) 

    @property
    def all_measures_list(self):
        opt_list = list()
        for table in self.bim["model"]["tables"]:
            if "measures" in table:
                #measures is a list
                measures = table["measures"]
                #check list length
                length = len(measures)
                for i in range(0, length):
                    opt_list.append(measures[i]["name"])
        return opt_list

    @property
    def all_visible_measures_list(self):
        #get all visible measures name(21rows)
        opt_list = list()
        for table in self.bim["model"]["tables"]:
            if "measures" in table:
                #measures is a list
                measures = table["measures"]
                #check list length
                length = len(measures)
                for i in range(0, length):
                    #next line means current measure is visible
                    if "isHidden" not in measures[i]:  
                        opt_list.append(measures[i]["name"]) 
        return opt_list
  
    @property
    def all_measures_hierarchy(self):
        measure_with_submeasure_dic = defaultdict(list) #571(rows) --> #576(rows)
        
        all_measures_list_upper_case = list()
        for measure in self.all_measures_list:
            all_measures_list_upper_case.append(str(measure).upper())
               
        for table in self.bim["model"]["tables"]:
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
                        if possible_measure.upper() in all_measures_list_upper_case:
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
        
        return measure_with_submeasure_list


    def write_load_data_script(self, file_name, full_table_name, column_name_list, value_list):
        file_name = file_name
        db_name, schema_name, table_name = full_table_name.split('.')
        column_count = len(column_name_list)
        value_fvalue_field_countiled_count = None

        file = open(file_name, mode = "w", encoding = "utf-8")  
        file.write(f"USE {db_name}\nGO\n")

        #set value field count
        if type(value_list) is list:
            if(type(value_list[0]) is list):
                value_field_count = len(value_list[0])
            elif (type(value_list[0]) is str):
                value_field_count = 1
            else:
                pass

        if column_count == value_field_count:
            if column_count==1:
                for x in value_list:
                    file.write(f"INSERT INTO {full_table_name}({column_name_list[0]}) VALUES (\'{x}\')\n")    
    
            #to_do need to be test
            if column_count>1:
                columns_str = ''
                #to-be --> [Measure], [Sub_Measure]
                for i in column_name_list:
                #concatenate the columns string  
                    if column_name_list[0] == i:
                        columns_str += f'{i}'
                    else:
                        columns_str += f', {i}'

                for row in value_list:
                #concatenate the values string 
                    values_str = ''
                    #to-be --> 'Active Customer Count', 'Active Customer Count Control_All'
                    for value in row:
                        if row[0] == value:
                            values_str += f"\'{value}\'"
                        else:
                            values_str += f", \'{value}\'" 
                    
                    file.write(f"INSERT INTO {full_table_name}({columns_str}) VALUES ({values_str})\n")

        else:
            print('column filed not match.')

        file.close()     

    @classmethod
    def write_bim(cls, bim_name, bim_content):
        #Cube.write_bim("opt_Model.bim", data)
        with open(bim_name, "w", encoding="utf-8") as opt_file:
            json.dump(bim_content, opt_file, indent=2)     


######################################################
acc_cube = Cube('ACC', "inp_Model.bim")


#print(type(acc_cube.all_measures_hierarchy))

# file_name, full_table_name, column_name, value
acc_cube.write_load_data_script(
    'opt_01_LoadData_All_Measures.sql', 
    '[DQ].[dbo].[Cube_All_Measure]',  
    ['[Measure]'], 
    acc_cube.all_measures_list
)

acc_cube.write_load_data_script(
    'opt_02_LoadData_All_Visible_Measures.sql', 
    '[DQ].[dbo].[Cube_Unhidden_Measure]',  
    ['[Measure]'], 
    acc_cube.all_visible_measures_list
)

acc_cube.write_load_data_script(
    'opt_03_LoadData_Measure_Hierarchy.sql', 
    '[DQ].[dbo].[Cube_Measure_Hierarchy]',  
    ['[Measure]', '[Sub_Measure]'], 
    acc_cube.all_measures_hierarchy
)




