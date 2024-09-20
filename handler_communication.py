def handle_communication(request_id, method, params):
    return success_response(request_id, method)


def success_response(request_id, method):
    if method == 'StartComm':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result":
            {
                "success": True,
                "data":
                {},
                "xtra":
                {
                    "retval": True
                }
            }
        }
    elif method == 'IsCommPortOpen':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "success": True,
                "xtra": {
                    "retval": True,
                },
                "data": True
            }
        }
    elif method == 'GetAppVersion':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result":
            {
                "success": True,
                "xtra":
                {
                    "retval": 50463234
                },
                "data": "3.2.2.2"
            }
        }
    elif method == 'EnumCommPorts':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result":
            {
                "success": True,
                "data": "preset"
            }
        }
    else:
        return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "success": True,
                    "xtra": {
                        "retval": True,
                    },
                    "data": True
                }
            }

def error_response(request_id, method):
    if method == 'StartComm':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result":
            {
                "xtra":
                {
                    "retval": False
                },
                "error":
                {
                    "code": -1,
                    "msg": "StartComm: Could not open the communication port (Error 0x848a0001: Connect string invalid.) !"
                },
                "success": False
            }
        }
    elif method == 'GetAppVersion':
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result":
            {
                "success": False,
                "xtra":
                {
                    "retval": False
                },
                "data": {}
            }
        }
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "success": True,
            "xtra": {
                "retval": False,
            },
            "data": False
        }
    }

