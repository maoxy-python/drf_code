import json

from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from apps.models import Student

"""
单个接口：获取单条 获取所有 增加单条 删除单条 整体更新单条 局部更新单条
群体：群增 群删 整体群该 局部群改
"""


@method_decorator(csrf_exempt, name="dispatch")
class StudentView(View):

    def get(self, request, *args, **kwargs):
        # 获取url中传递的参数
        pk = kwargs.get("pk")
        if not pk:  # 查询全部
            stu_list = Student.objects.all().values("name", "password")
            return JsonResponse({
                "status": 200,
                "message": "success",
                "result": list(stu_list),
            }, json_dumps_params={"ensure_ascii": False})
        else:  # 查询单条
            stu_obj = Student.objects.filter(pk=pk).values("name", "password").first()
            if stu_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "success",
                    "result": stu_obj,
                }, json_dumps_params={"ensure_ascii": False})
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "fail",
                }, json_dumps_params={"ensure_ascii": False})

        # return JsonResponse({"message": "GET方法"})

    def post(self, request, *args, **kwargs):
        print(request.body)
        print(request.POST)
        try:
            stu_obj = Student.objects.create(**request.POST.dict())
            if stu_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "success",
                    "result": {"name": stu_obj.name, "pwd": stu_obj.password},
                }, json_dumps_params={"ensure_ascii": False})
        except:
            return JsonResponse({
                "status": 500,
                "message": "fail",
            }, json_dumps_params={"ensure_ascii": False})
        # return JsonResponse({"message": "POST方法"})

    def put(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        print(put.get("name"))
        return JsonResponse({"message": "PUT方法"})


class UserView(APIView):
    renderer_classes = [BrowsableAPIRenderer]
    def get(self, request, *args, **kwargs):
        print(request._request.GET)
        print(request.GET)
        print(request.query_params)
        return Response("DRF Ready!")

    def post(self, request, *args, **kwargs):
        print(request._request.POST)
        print(request.POST)
        print(request.data)
        return Response("DRF POST")

    def put(self, request, *args, **kwargs):
        print(request.data)
        return Response("DRF POST")

    def delete(self, request, *args, **kwargs):
        print(request.data)
        return Response("DRF POST")


class UserView2(APIView):

    def get(self, request, *args, **kwargs):
        print(request._request.GET)
        print(request.GET)
        print(request.query_params)
        return Response("DRF Ready!")

    def post(self, request, *args, **kwargs):
        print(request._request.POST)
        print(request.POST)
        print(request.data)
        return Response("DRF POST")
