from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    # 基表的声明  不在数据库创建对应的表
    class Meta:
        abstract = True


class Book(BaseModel):
    """book_name、price、pic、authors、publish、is_delete、create_time、status"""
    book_name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pic = models.ImageField(upload_to="img", default="img/2.jpg")
    publish = models.ForeignKey(to="Press", on_delete=models.CASCADE, db_constraint=False, related_name="books")
    authors = models.ManyToManyField(to="Author", db_constraint=False, related_name="books")

    class Meta:
        db_table = "bz_book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name

    # 自定义额外的属性
    def example(self):
        return "example"

    # 自定义类属性
    @property
    def publish_name(self):
        return self.publish.press_name

    @property
    def author_list(self):
        return self.authors.values("author_name", "age", "detail__phone")


class Press(BaseModel):
    press_name = models.CharField(max_length=128)
    pic = models.ImageField(upload_to="img", default="img/2.jpg")
    address = models.CharField(max_length=256)

    class Meta:
        db_table = "bz_press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name


class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    age = models.IntegerField()

    class Meta:
        db_table = "bz_author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name


class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author", on_delete=models.CASCADE, related_name="detail")

    class Meta:
        db_table = "bz_author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name
