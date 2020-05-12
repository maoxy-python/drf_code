from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import APISettings
from rest_framework.parsers import parse, JSONParser

from apps.models import Student


class StudentView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        print("GET方法")
        stu_id = kwargs.get("pk")
        if stu_id:
            # stu_dic = Student.objects.filter(pk=stu_id).values("name", "password").first()
            # 此时发生异常 使用异常模块处理
            stu_obj = Student.objects.get(pk=stu_id)
            return Response({
                "status": 200,
                "message": "success",
                "result": {
                    "name": stu_obj.name,
                    "password": stu_obj.password
                },
            })

        return Response("GET方法已访问")

    def post(self, request, *args, **kwargs):
        print("POST方法")
        # 传参数的方式只有url拼接一种
        print(request.query_params)
        # 传参方式：form  encoding json
        print(request.data)
        return Response("POST方法已访问")


from rest_framework import serializers