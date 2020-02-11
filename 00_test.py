
# columns_str_1 = '[Measure],'*3

# x = '[Measure]'
# columns_str = f'{x}'
# columns_str *=3
# print(columns_str)


# list = ['[Measure]','[Sub_Measure]']
# columns_str = ''
# for i in list:
#     if list[0] == i:
#         columns_str += f'{i}'
#     else:
#         columns_str += f', {i}'


# print(columns_str)#


nest_list = [['Active cusotmer count', 'Active customer count_Control'], ['Active customer count_Control', 'Active customer count_All']]
values_str = ''
for row in nest_list:
    values_str = ''
    for value in row:
        if row[0] == value:
            values_str += f"\'{value}\'"
        else:
            values_str += f", \'{value}\'" 


print(values_str)