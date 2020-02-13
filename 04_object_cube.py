import json
from collections import defaultdict


class Cube:

    cube_count = 0                      #for check how many Cube instance
    
    def __init__(self, name, file_name):
        super().__init__()
        self.name = name
        self.file_name = file_name
        self.bim = dict()               #self.bim not use property decorators due to two reasons, first, performance issue when deleting, second, DELETE statement is not success
        Cube.cube_count += 1

    @property
    def all_measures_list(self):
        """
        post-condition: return and set property all_measures_list as a list
        """
        opt_list = list()
        for table in self.bim["model"]["tables"]:
            if "measures" in table:
                measures = table["measures"]    #measures is a list
                length = len(measures)
                for i in range(0, length):
                    opt_list.append(measures[i]["name"])
        return opt_list

    @property
    def all_visible_measures_list(self):
        """
        post-condition: return and set property all_visible_measures_list as a list
        """        
        opt_list = list()
        for table in self.bim["model"]["tables"]:
            if "measures" in table:
                measures = table["measures"]    #measures is a list
                length = len(measures)
                for i in range(0, length):
                    if "isHidden" not in measures[i]:
                        #add visible measure
                        opt_list.append(measures[i]["name"]) 
        return opt_list
  
    @property
    def all_measures_hierarchy(self):
        """
        all_measures_hierarchy is a nested list     ex. [['aaa','bbb'],['bbb','ccc']...]
        post-condition: return and set property all_visible_measures_list as a nested list
        """
        measure_with_submeasure_dic = defaultdict(list)
        
        all_measures_list_upper_case = list()
        for measure in self.all_measures_list:
            all_measures_list_upper_case.append(str(measure).upper())
               
        for table in self.bim["model"]["tables"]:
            if "measures" in table:
                measures = table["measures"]    #measures is a list
                length = len(measures)
                for i in range(0, length):

                    measure_name = str(measures[i]["name"])
                    #get expression like [ ......[].....[]....]
                    expres = str(measures[i]["expression"])
                    if expres.count("[") > 1:
                        #strip first and last '[' & ']'
                        expres = expres[1:len(expres)-1]

                    #if measure_name.upper() == "Partner Retention Rate (YoY)_Org".upper():
                    #check how many possible measures
                    while expres.find("[") >= 0 and expres.find("]") >= 0:
                        start_num = expres.find("[")+1
                        end_num = expres.find("]")
                        possible_measure = expres[start_num: end_num]                    
                        #add to dic if match
                        if possible_measure.upper() in all_measures_list_upper_case:

                            #add to dic
                            sub_measure_group_up = [ x.upper() for x in measure_with_submeasure_dic[measure_name] ]
                            #sub_measure_group = measure_with_submeasure_dic[measure_name]
                            if sub_measure_group_up == None:
                                measure_with_submeasure_dic[measure_name].append(possible_measure)
                            else:
                                #skip if the value is existing
                                if possible_measure.upper() not in sub_measure_group_up:
                                    measure_with_submeasure_dic[measure_name].append(possible_measure)

                        #curtail string
                        expres = expres[end_num+1:len(expres)]
        
        measure_with_submeasure_list = []
        for x in measure_with_submeasure_dic:
            value_list = measure_with_submeasure_dic.get(x)
            for i in value_list:
                measure_with_submeasure_list.append([x, i])

        measure_with_submeasure_list.sort() 
        
        return measure_with_submeasure_list

    def set_bim(self):
        data_str = open(self.file_name, encoding="utf-8").read()     
        self.bim = json.loads(data_str) 

    def write_load_data_script(self, file_name, full_table_name, column_name_list, value_list):
        """
        input:
            1. [output file name]
            2. [sql server full table name] ex.[DQ].[dbo].[Cube_Unhidden_Measure]
            3. [list of column name]
            4. [nested list of value]       ex. [['aaa','bbb'],['bbb','ccc']...]
        output:
            1. [insert sctipt for sql server]
        """
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
            print('count of column and count of value_filed are not match.')

        file.close()     

    def delete_measures(self, to_be_deleted_measures_list):
        """
        pre-condition:
        post-condition: delete useless measures and update Cube.bim 
        """
        #arrange to be delete scope
        file_path = to_be_deleted_measures_list
        to_be_delete_list = []
        with open(file_path, mode = "r", encoding = "utf-8") as file:
            line_measure = file.readline()
            cnt = 1
            while line_measure:
                to_be_delete_list.append(line_measure.strip())
                #read next line
                line_measure = file.readline()

        file.close()   

        del_num_dict = defaultdict(list)
        table_length = len(self.bim["model"]["tables"])

        #check delete scope
        for x in range(0, table_length):
            if "measures" in self.bim["model"]["tables"][x]:
                #measures is a list
                measures = self.bim["model"]["tables"][x]["measures"]
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
                del self.bim['model']['tables'][table_num]['measures'][measure_num]

    @classmethod
    def write_bim(cls, bim_name, bim_content):
        """
        input: 
            1. [output file name]
            2. [data of bim]
        output:
            1. [file of bim]
        """
        with open(bim_name, "w", encoding="utf-8") as opt_file:
            json.dump(bim_content, opt_file, indent=2)     

def main():

    # initial
    acc_cube = Cube('ACC', "inp_Model.bim")
    acc_cube.set_bim()

    # create load data scripts
    # file_name, full_table_name, column_name_list, value_list
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

    # update Cube.bim
    acc_cube.delete_measures('inp_to_be_deleted_measures_list.txt')

    Cube.write_bim('opt_Model.bim', acc_cube.bim)

if __name__ == '__main__':
    main()