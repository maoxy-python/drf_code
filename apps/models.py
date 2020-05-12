from django.db import models


# Create your models here.


class Student(models.Model):
    sex_choices = (
        (0, "male"),
        (1, "female"),
        (2, "others"),
    )

    name = models.CharField(max_length=40)
    password = models.CharField(max_length=128, blank=True, null=True)
    sex = models.SmallIntegerField(choices=sex_choices, default=1)

    class Meta:
        db_table = "bz_student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
