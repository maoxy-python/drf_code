from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, data_status=0, data_message=0, results=None,
                 http_status=None, headers=None, exception=False, **kwargs):
        # data 的初始状态
        data = {
            "status": data_status,
            "message": data_message,
        }
        # result 可能是False 0 等数据，这些数据在某些情况下可以作为合法数据返回
        if results is not None:
            data['results'] = results

        # data响应的其他内容
        # if kwargs is not None:
        #     for k, v in kwargs.items():
        #         setattr(data, k, v)
        data.update(kwargs)

        # 拿到的是Response对象
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)


"""
原有的返回值
Response({
    "status":0,
    "message": "success",
    "results": [],
    "token":"",
}, status=http_status,headers=headers,exception=True|False)

APIResponse() => Response({"status":0,"message": "success",})
"""
