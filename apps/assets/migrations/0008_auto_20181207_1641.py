# Generated by Django 2.1.3 on 2018-12-07 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20181207_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttylog',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='命令执行时间'),
        ),
    ]