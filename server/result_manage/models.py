from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone



# 模型测试任务
class TestResult(models.Model):
    # 测试结果id号，唯一 允许为空
    result_id = models.IntegerField(null=True, verbose_name="测试结果id号")
    # 用户id号 允许为空
    user_id = models.IntegerField(null=True, verbose_name="用户id号")
    # 测试任务id号，唯一 允许为空
    test_task_id = models.IntegerField(null=True, verbose_name="文件id号")
    # 结果路径
    result_path = models.CharField(max_length=256, verbose_name="结果路径")




# iou数据
class IouData(models.Model):
    # iou数据id号，唯一 允许为空
    data_id = models.IntegerField(null=True, verbose_name="测试结果id号")

    result_id = models.IntegerField(null=True, verbose_name="测试结果id号")

    ego_id = models.IntegerField(null=True, verbose_name="中心车辆id号")
    # 分开扩增时，这个哪个车单独扩增的结果，为0时代表为分开扩增
    car_id = models.IntegerField(null=True, verbose_name="测试结果id号")
    # 帧数
    frame_id = models.IntegerField(null=True, verbose_name="帧数")
    # 'raw' 'aug'
    data_type = models.CharField(max_length=256, verbose_name="结果路径")

    road_iou = models.FloatField(null=True)

    lane_iou = models.FloatField(null=True)

    dynamic_iou = models.FloatField(null=True)