# Generated by Django 3.0 on 2020-05-09 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('author_name', models.CharField(max_length=128)),
                ('age', models.IntegerField()),
            ],
            options={
                'verbose_name': '作者',
                'verbose_name_plural': '作者',
                'db_table': 'bz_author',
            },
        ),
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('press_name', models.CharField(max_length=128)),
                ('pic', models.ImageField(default='img/2.jpg', upload_to='img')),
                ('address', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': '出版社',
                'verbose_name_plural': '出版社',
                'db_table': 'bz_press',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('book_name', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pic', models.ImageField(default='img/2.jpg', upload_to='img')),
                ('authors', models.ManyToManyField(to='api_model_ser.Author')),
                ('publish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_model_ser.Press')),
            ],
            options={
                'verbose_name': '图书',
                'verbose_name_plural': '图书',
                'db_table': 'bz_book',
            },
        ),
        migrations.CreateModel(
            name='AuthorDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=11)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_model_ser.Author')),
            ],
            options={
                'verbose_name': '作者详情',
                'verbose_name_plural': '作者详情',
                'db_table': 'bz_author_detail',
            },
        ),
    ]
