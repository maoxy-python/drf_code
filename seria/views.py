from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from seria.models import Employee


class EmployeeAPIVIew(APIView):

    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get("pk")
        if emp_id:
            try:
                # 用户对象无法直接返回到前台 因为无法序列化
                emp_obj = Employee.objects.get(pk=emp_id)
                # TODO 在返回数据之前对用户数据进行序列化
                emp_ser = serializers.EmployeeSerializer(emp_obj).data
                print(emp_ser)
                return Response({
                    "status": 200,
                    "message": "success",
                    "result": {
                        "emp_obj": emp_ser
                    }
                })
            except:
                return Response({
                    "status": 500,
                    "message": "user is not exists",
                })
        else:
            # 同样无法序列化
            emp_list = Employee.objects.all()
            # TODO 此时需要DRF的序列化组件完成序列化的作用  之前是手动转换
            emp_ser = serializers.EmployeeSerializer(emp_list, many=True).data
            return Response({
                "status": 200,
                "message": "success",
                "result": {
                    "emp_obj": emp_ser
                }
            })

    def post(self, request, *args, **kwargs):

        request_data = request.data

        # 验证数据类型是否合法 是否是字典 单个对象
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 500,
                "message": "data is not error",
            })

        # 校验数据内容是否合法  参与反序列化的数据需要赋值给data
        deserializer = serializers.EmployeeDeserializer(data=request_data)
        # print(deserializer)
        # 返回值为 True校验成功  is_valid()方法完成校验  校验失败的信息会保存在 .errors中
        if deserializer.is_valid():
            print(deserializer.is_valid())
            # 通过完成新增
            emp_obj = deserializer.save()
            # print(emp_obj)
            return Response({
                "status": 500,
                "message": "success",
                "result": serializers.EmployeeSerializer(emp_obj).data
            })
        else:
            # 校验失败
            return Response({
                "status": 500,
                "message": deserializer.errors,
            })
