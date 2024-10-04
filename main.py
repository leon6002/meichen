import asyncio
import traceback
import websockets
import json
import random

from handler_communication import handle_communication
from handler import handle_multi_read, handle_read, handle_write
from read_local_data import read_json
saved_param = {}
subscriptions = {}  # 用于存储订阅信息
local_data = read_json()

async def send_updates(websocket, subId, params):
    interval = params[1]/1000  # 默认间隔为1秒
    print('interval is: ', interval)
    variable_name = params[0] # 假设params中有要订阅的变量名

    while True:
        try:
            print('sending')
            # 获取当前变量值（这里假设local_data是一个字典）
            method_str = local_data[variable_name]["method"]
            value = eval(method_str)
            # 构建响应消息并发送
            update_message = {"jsonrpc":"2.0","method":"OnVariableChanged","params":[variable_name,subId,value]}
            await websocket.send(json.dumps(update_message))

            await asyncio.sleep(interval)  # 等待指定的时间间隔
        except Exception as e:
            print(f"发送更新时发生错误: {e}")
            break

async def handle_message(websocket, path):

    async for message in websocket:
        try:
            # 解析收到的消息
            request = json.loads(message)
            # 检查请求的完整性
            if "jsonrpc" in request and "method" in request and "id" in request:
                method = request["method"]
                request_id = request["id"]
                print(f"收到请求: { request_id}")
                params = request.get("params", [])
                if method in ["IsCommPortOpen", "StartComm","StopComm", "GetAppVersion", "EnumCommPorts"]:
                    response = handle_communication(request_id, method, params)
                # 根据method处理不同的请求，这里只处理ReadVariable方法
                elif method == "ReadVariable":
                    response = handle_read(request_id, params, local_data, saved_param)
                elif method == "ReadMultipleVariables":
                    response = handle_multi_read(request_id,params, local_data, saved_param)
                elif method == "WriteVariable":
                    response = handle_write(request_id, params, local_data, saved_param)
                elif method == "EnableEvents":
                    response ={"jsonrpc":"2.0","id":str(request_id),"result":{"success":True,"data":{}}}
                elif method == "SubscribeVariable":
                    if websocket not in subscriptions:
                        subscriptions[websocket] = []
                    subId = len(subscriptions)
                    subscriptions[websocket].append(asyncio.create_task(send_updates(websocket, subId, params)))
                    response = {"jsonrpc":"2.0","id":str(request_id),"result":{"success":True,"data":{},"xtra":{"subscriptionId":subId}}}
                elif method == 'UnSubscribeVariable':
                    if websocket in subscriptions:
                        for task in subscriptions[websocket]:
                            task.cancel()  # 取消所有相关任务
                        del subscriptions[websocket]
                    response = {"jsonrpc":"2.0","id":str(request_id),"result":{"success":True,"data":{},"xtra":{"retval":1}}}
                else:
                    # 不支持的method，返回错误
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -1,
                            "message": "Method not found"
                        }
                    }
            else:
                # 无效的请求，返回错误
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request"
                    }
                }

            # 发送响应
            response_message = json.dumps(response)
            # print(f"发送响应: {response_message}")
            await websocket.send(response_message)

        except json.JSONDecodeError:
            # JSON解析错误，返回错误
            response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            await websocket.send(json.dumps(response))
        except Exception as e:
            # 处理其他异常
            traceback.print_exc()
            print(f"发生错误: {e}")
            response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
            await websocket.send(json.dumps(response))

# 启动WebSocket服务器
start_server = websockets.serve(handle_message, '0.0.0.0', 41001)

print("WebSocket服务器已启动，正在监听端口41000...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()