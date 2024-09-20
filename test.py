import json
import random

# import random
# tmp = random.uniform(0,10)
# rounded_tmp = round(tmp, 6)
# result_str = str(rounded_tmp)
# print("tmp = ",tmp)
# print("result_str = ",result_str)


# import json

# names = ['stiffness_variables.json', 'main_variables.json', 'cdc_variables.json', 'main_warnings.json', 'ui_control.json']

# filename = names[4]
# with open(filename, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# new_data = {}
# for item in data: 
#   item['method'] = 'random.uniform(0,100)'
#   #只读4， 只写2， 可读写6
#   item['access'] = 6
#   new_data[item['name']] = item
# # 保存new_data为json文件
# with open('new_'+filename, 'w', encoding='utf-8') as f:
#     json.dump(new_data, f, ensure_ascii=False, indent=4)
# print("新的JSON文件已保存")

# test method eval


# with open('new_stiffness_variables.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
# method_str = data["PWM_FCE2_0_DW.Emer_Brake_Pedal"]["method"]
# print("method_str = ",method_str)
# print(eval(method_str))


# extract variables
# with open('main_warnings.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
# names = [d['label'] for d in data]
# print(names)


with open('cdc_variables.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for d in data:
        d['range'] = {"min": -1000, "max": 1000}
print(data)