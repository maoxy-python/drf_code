from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api_model_ser import serializers
from api_model_ser.models import Book, Press
from utils.response import APIResponse


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookModelSerializer(book_obj).data
                return Response({
                    "status": 200,
                    "message": "success",
                    "results": book_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "book not exists",
                })
        else:
            book_list = Book.objects.all()
            book_ser = serializers.BookModelSerializer(book_list, many=True).data

        return Response({
            "status": 200,
            "message": "success",
            "results": book_ser,
        })

    def post(self, request, *args, **kwargs):
        """只考虑增加单个"""
        request_data = request.data
        book_ser = serializers.BookModelDeserializer(data=request_data)
        # raise_exception=True：当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)  # 检验是否合格 raise_exception=True必填的
        book_obj = book_ser.save()  # 保存得到一个对象
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookModelSerializer(book_obj).data
        })


class PressAPIView(APIView):

    def get(self, request, *args, **kwargs):
        press_id = kwargs.get("id")

        if press_id:
            try:
                press_obj = Press.objects.get(pk=press_id)
                press_ser = serializers.PressModelSerializer(press_obj).data
                return Response({
                    "status": 200,
                    "message": "success",
                    "results": press_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "book not exists",
                })
        else:
            press_list = Press.objects.all()
            press_ser = serializers.PressModelSerializer(press_list, many=True).data

        return Response({
            "status": 200,
            "message": "success",
            "results": press_ser,
        })


class BookAPIView2(APIView):

    def get(self, request, *args, **kwargs):
        """ 单查 群查 """
        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookSerializerV2(book_obj).data
                return Response({
                    "status": 200,
                    "message": "success",
                    "results": book_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "book not exists",
                })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_ser = serializers.BookSerializerV2(book_list, many=True).data

        return Response({
            "status": 200,
            "message": "success",
            "results": book_ser,
        })

    def post(self, request, *args, **kwargs):
        """只考虑增加单个"""
        """修改群增多个"""
        request_data = request.data

        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 500,
                "message": "数据有问题",
            })

        book_ser = serializers.BookSerializerV2(data=request_data, many=many)  # 反序列化
        # raise_exception=True：当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)  # 检验是否合格 raise_exception=True必填的
        book_obj = book_ser.save()  # 保存得到一个对象
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookSerializerV2(book_obj, many=many).data
        })

    # 单删：有id  通过postman路径传参
    # 群删：有多个id  json传参
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if Book.objects.filter(pk__in=pks, is_delete=False).update(is_delete=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

    # 单整体改：修改所有字段
    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get('id')

        try:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
        except:
            return Response({
                'status': 0,
                'msg': '修改时图书不存在',
                'results': ""
            })

        # 前台要提供修改的数据，修改之后保存的数据需要校验，校验的数据应该在实例化“序列化类对象”时，赋值给data方便钩子函数校验
        book_ser = serializers.BookSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)

        # 校验通过 完成数据的更新，获取要更新的目标
        book_ser.save()

        return Response({
            'status': 0,
            'msg': 'PUT SUCCESS',
            'results': serializers.BookSerializerV2(book_obj).data
        })

    """
    # 单局部改：修改部分字段
    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get('id')

        try:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
        except:
            return Response({
                'status': 0,
                'msg': '修改时图书不存在',
                'results': ""
            })

        # 前台要提供修改的数据，修改之后保存的数据需要校验，校验的数据应该在实例化“序列化类对象”时，赋值给data方便钩子函数校验
        book_ser = serializers.BookSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)

        # 校验通过 完成数据的更新，获取要更新的目标
        book_ser.save()

        return Response({
            'status': 0,
            'msg': 'PUT SUCCESS',
            'results': serializers.BookSerializerV2(book_obj).data
        })
    """

    # 群局部改
    def patch(self, request, *args, **kwargs):
        request_data = request.data
        pk = kwargs.get("id")

        # 将单改，群改的数据进行格式化 pks = [需要的对象主键标识] | request_data = [每个要修改的对象对应的修改数据]
        if pk and isinstance(request_data, dict):
            # 代表单改  改为群改一个
            pks = [pk, ]
            request_data = [request_data, ]
        elif not pk and isinstance(request_data, list):
            # 代表群改
            pks = []
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    pks.append(pk)
                else:
                    return Response({
                        'status': 505,
                        'msg': 'PK有误',
                        'results': ""
                    })
        else:

            return Response({
                'status': 505,
                'msg': '数据有误',
                'results': ""
            })
        # 对pks与request_data进行数据筛选
        # 将pks中不存在的对象的pk进行移除，request_data对应的数据也移除
        # 将pks中的pk查询出对应的对象
        objs = []
        new_data = []
        for index, pk in enumerate(pks):
            try:
                # pk对应的数据如果存在则储存
                obj = Book.objects.get(pk=pk, is_delete=False)
                # print(obj, type(obj))
                objs.append(obj)
                # 对应索引的数据需要保存
                new_data.append(request_data[index])
            except:
                # 不存在则从request_data中移除 问题：移除会有问题，在不断的pop中数据越来越少  下标不准确
                # index = pks.index(pk)  # 获取pk的索引
                # request_data.pop(index)
                continue

        # print(pks)
        # print(request_data)

        # 无论是单改还是群改都走 群改
        book_ser = serializers.BookSerializerV2(data=new_data, instance=objs, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)

        # 校验通过 完成数据的更新，获取要更新的目标
        book_objs = book_ser.save()

        # 下面封装了Response
        # return Response({
        #     'status': 200,
        #     'msg': 'SUCCESS',
        #     'results': serializers.BookSerializerV2(book_objs, many=True).data
        # })
        results = serializers.BookSerializerV2(book_objs, many=True).data

        # 采用自定义二次封装响应数据
        return APIResponse(1, "我成功了", results=results)


class BookGenericAPIView(GenericAPIView):
    pass
