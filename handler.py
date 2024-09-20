import json
import random

from read_local_data import read_json

def handle_read(request_id, params, local_data, saved_param):
    variable_name = params[0] if params else None
    if variable_name:
        value = 0
        if variable_name in saved_param:
           value = saved_param[variable_name]
        else:
           # 模拟读取变量的值
           method_str = local_data[variable_name]["method"]
           value = eval(method_str)
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "success": True,
                "xtra": {
                    "retval": True,
                    "formatted": format_data(value)
                },
                "data": value
            }
        }
    else:
        # 缺少参数，返回错误
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -1,
                "message": "Invalid params"
            }
        }
    return response

def random_warning():
    return random.choice(generate_fixed_sequence(100,1))
def generate_fixed_sequence(num_zeros, num_ones):
    if num_ones == 0:
        return [0] * num_zeros
    
    # 创建初始序列，每个 '1' 后面跟着 'num_zeros' 个 '0'
    sequence = []
    
    for _ in range(num_ones):
        sequence.append(1)
        sequence.extend([0] * num_zeros) 
    
    # 如果需要，可以去掉最后多余的零
    if len(sequence) > (num_ones - 1) * (num_zeros + 1):
        sequence = sequence[:-num_zeros]
    
    return sequence
def handle_multi_read(request_id, params, local_data, saved_param):
    variable_names = params[0] if params else None
    datas = []
    for variable_name in variable_names:
        value = 0
        if variable_name in saved_param:
           value = saved_param[variable_name]
        else:
           # 模拟读取变量的值
            method_str = local_data[variable_name]["method"]
            if method_str == 'random_warning()':
                if variable_name == 'PWM_FCE2_0_DW.TemperaWarm':
                    value = random.choice([0])
                else: 
                    value = 0
            else:
                value = eval(method_str)

        var_data = {
           "name": variable_name, 
           "value": value,
           "formatted": format_data(value),
           "status": 1,
           "retMsg": ""
        }
        datas.append(var_data)
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "success": True,
            "xtra": {
                "retval": len(datas)
            },
            "data": json.dumps(datas, ensure_ascii=False)
            }
    }
    return response

def handle_write(request_id, params, local_data, saved_param):
    variable_name = params[0] if params else None
    variable_value = float(params[1]) if params else None
    if variable_name:
        # 模拟读取变量的值，这里直接返回示例值
        value = variable_value
        if variable_name == 'PWM_FCE2_0_DW.Aerate_Tank':
           saved_param['PWM_FCE2_0_DW.pump_relay'] = value
        if variable_name.startswith('PWM_FCE2_0_DW.Level') and len(variable_name) == 20:
           saved_param['PWM_FCE2_0_DW.test_levelOut'] = int(variable_name[-1])
        saved_param[variable_name] = value

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "success": True,
                "xtra": {
                    "retval": True,
                    "formatted": f"{value:.6f}"
                },
                "data": value
            }
        }
    else:
        # 缺少参数，返回错误
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -1,
                "message": "Invalid params"
            }
        }

    return response

def format_data(value):
  if isinstance(value, float):  # 判断是否为浮点数
    return round(value, 6)  # 保留6位小数
  else:
    return str(value)  # 如果不是浮点数，返回字符串


if __name__ == "__main__":
   _local_data = read_json()
#    res = handle_read(1, ["PWM_FCE2_0_DW.exhaust_error[2]"], _local_data)
   res = handle_multi_read(1, [["PWM_FCE2_0_DW.exhaust_error[2]", "PWM_FCE2_0_DW.exhaust_error[1]"]], _local_data)
   print(res)