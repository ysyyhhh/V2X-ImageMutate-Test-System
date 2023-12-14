# Generated by Django 3.2.19 on 2023-09-03 09:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AugConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_id', models.IntegerField(null=True, verbose_name='任务id号')),
                ('default_flag', models.BooleanField()),
                ('aug_type', models.CharField(max_length=64, verbose_name='扩增类型')),
                ('aug_para', models.IntegerField(null=True, verbose_name='扩增参数')),
                ('ego_car_id', models.IntegerField(default=0, null=True, verbose_name='中心车辆id号')),
                ('separate_flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AugTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(null=True, verbose_name='任务id号')),
                ('task_name', models.CharField(max_length=256, verbose_name='任务名称')),
                ('user_id', models.IntegerField(null=True, verbose_name='用户id号')),
                ('raw_file_id', models.IntegerField(null=True, verbose_name='文件id号')),
                ('aug_file_id', models.IntegerField(null=True, verbose_name='扩增完成文件id号')),
                ('task_state', models.CharField(max_length=64, verbose_name='文件状态')),
                ('config_id', models.IntegerField(null=True, verbose_name='扩增配置id号')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
            ],
        ),
    ]