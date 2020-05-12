from rest_framework import serializers, exceptions

from drf_code import settings
from seria.models import Employee


class EmployeeSerializer(serializers.Serializer):
    """
    为每一个model类编写一个序列化器，与django的Form相似
    """
    username = serializers.CharField()
    phone = serializers.CharField()
    # sex = serializers.IntegerField()

    # 这个数据可以在数据库不存在  叫作自定义序列化属性
    # example = serializers.SerializerMethodField()
    # 自定义性别
    gender = serializers.SerializerMethodField()

    # 自定义图片类型的序列化  返回完成的url
    img = serializers.SerializerMethodField()

    # 此时可序列化
    def get_img(self, obj):
        # print(obj.img, type(str(obj.img)))

        # return "http://127.0.0.1:8000" + settings.MEDIA_URL + str(obj.head_pic)
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.img))

    def get_example(self, obj):
        # print(self, type(self))
        # print(obj, type(obj))
        return "123"

    def get_gender(self, obj):
        return obj.get_sex_display()


class EmployeeDeserializer(serializers.Serializer):
    """
    反序列化：将用户提交的数据存入数据库
    1. 哪些字段必须反序列化
    2. 字段的安全校验
    3. 哪些字段需要额外提供校验
    4. 哪些字段存在联合校验
    反序列化字段是用来入库的，不存在自定义字段
    """
    username = serializers.CharField(
        max_length=20,
        min_length=10,
        error_messages={
            'max_length': "长度过长",
            'min_length': "长度过短",
        },
        write_only=True
    )
    password = serializers.CharField(write_only=True, required=True)
    # 自定义有校验规则的反序列化字段
    phone = serializers.CharField(required=False, write_only=True)
    sex = serializers.IntegerField(write_only=True)
    re_pwd = serializers.CharField(write_only=True, required=True)

    # 局部钩子 validate_"需要校验的字段"  通过返回原值 失败抛出异常
    def validate_username(self, value):
        # print("value:", value)
        if "1" in value.lower():  # 演示异常
            raise exceptions.ValidationError("用户名异常")
        return value

    # create()方法之前使用全局钩子函数validate()方法校验数据  对全部字段校验
    def validate(self, attrs):
        print(attrs)
        pwd = attrs.get('password')
        re_pwd = attrs.pop('re_pwd')
        if len(pwd) < 6:
            raise exceptions.ValidationError("密码过短")
        return attrs

    # 完成新增需要重写create方法
    def create(self, validated_data):
        print(validated_data)
        # 在所有校验规则完毕后可以直接入库
        return Employee.objects.create(**validated_data)
