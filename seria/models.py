from django.db import models


# Create your models here.


class Employee(models.Model):
    SEX_CHOICES = [
        [0, '男'],
        [1, '女'],
    ]

    username = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=11, null=True, default=None)
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    img = models.ImageField(upload_to='img', default='img/2.jpg')

    class Meta:
        db_table = 'bz_employee'
        verbose_name = '员工'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % self.username
