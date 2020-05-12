from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ListSerializer

from api_model_ser.models import Book, Press


class PressModelSerializer(ModelSerializer):
    class Meta:
        # 指定要序列化的类
        model = Press
        # 指定序列化类的哪些自字段
        fields = ("press_name", "address")


class BookModelSerializer(ModelSerializer):
    # 自定义连表序列化查询 出版社的信息  可嵌套序列化器来查询
    publish = PressModelSerializer()

    # 也可在此处自定义提供字段
    press_address = SerializerMethodField()

    def get_press_address(self, obj):
        return obj.publish.address

    class Meta:
        # 指定要序列化的类
        model = Book
        # 指定序列化类的哪些自字段
        fields = ("book_name", "price", "example", "publish_name", "author_list", "press_address", "publish")

        # 可以直接序列化全部字段
        # fields = "__all__"

        # 指定不展示哪些字段
        # exclude = ("id", "is_delete", "status")

        # 指定关联表的序列化深度
        # depth = 1


# 反序列化  入库
class BookModelDeserializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "authors", "publish", "pic")

        # 可以添加系统反序列化的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 1,  # 设置最小长度
                "error_messages": {
                    "required": "必填项",
                    "min_length": "太短"
                }
            }
        }

    # 局部钩子 校验图书名
    def validate_book_name(self, value):
        # 检查图书名是否已经存在
        if "a" in value.lower():
            raise ValidationError("a图书已存在")
        else:
            return value

    def validate(self, attrs):
        publish = attrs.get('publish')  # publish如果是外键字段，这个就是publish对象
        name = attrs.get('book_name')
        book_obj = Book.objects.filter(book_name=name, publish=publish)
        if book_obj:
            raise ValidationError("该出版社以及出版过该图书")
        return attrs


"""
1) fields中设置所有序列化与反序列化字段
2) extra_kwargs划分只序列化或只反序列化字段（
一般我们把需要存入到数据库中的使用write_only（反序列化）,只需要展示的就read_only(序列化)，看需求设计）
3) 设置反序列化所需的 系统、局部钩子、全局钩子 等校验规则
"""


class BookListSerializerV2(ListSerializer):
    def update(self, instance, validated_data):
        # print(instance)  # 需要更新的对象们
        # print(validated_data)  # 更新对应所需的数据
        # print(self.child)  # 服务的的模型序列化类-指得就是BookSerializerV2
        # return [
        #     self.child.update(instance, validated_data) for attrs in validated_data
        # ]
        # 调用ListSerializer的update方法进行修改 而这个update方法会调用ModelSerializer的update方法
        for index, obj in enumerate(instance):
            print(index, obj)
            self.child.update(obj, validated_data[index])
        return instance


class BookSerializerV2(ModelSerializer):
    class Meta:
        model = Book
        # 取序列化与反序列化所有字段的并集
        fields = ('book_name', 'price', 'pic', 'author_list', 'publish_name', 'publish', 'authors')
        extra_kwargs = {
            'book_name': {
                'required': True,
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短',
                }
            },
            'publish': {
                'write_only': True  # 只参与序列化的字段
            },
            'authors': {
                'write_only': True
            },
            'img': {
                'read_only': True,
            },
            'author_list': {
                'read_only': True,
            },
            'publish_name': {
                'read_only': True,
            }
        }

        # 群改需要设置自定义ListSerializer 重写群改的update方法
        list_serializer_class = BookListSerializerV2

    # 局部钩子 校验图书名
    def validate_book_name(self, value):
        # 检查图书名是否已经存在
        if "a" in value.lower():
            raise ValidationError("a图书已存在")
        else:
            return value

    def validate(self, attrs):
        publish = attrs.get('publish')  # publish如果是外键字段，这个就是publish对象
        name = attrs.get('book_name')
        book_obj = Book.objects.filter(book_name=name, publish=publish)
        if book_obj:
            raise ValidationError("该出版社以及出版过该图书")
        return attrs
