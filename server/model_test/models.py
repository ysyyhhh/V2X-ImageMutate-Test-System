from django.db import models
from django.utils import timezone



# 模型测试任务
class ModelTestTask(models.Model):
    # 任务id号，唯一 允许为空
    task_id = models.IntegerField(null=True, verbose_name="任务id号")
    # 任务名称
    task_name = models.CharField(max_length=256, verbose_name="任务名称")
    # 用户id号 允许为空
    user_id = models.IntegerField(null=True, verbose_name="用户id号")
    # 测试结果id号 允许为空
    result_id = models.IntegerField(null=True, verbose_name="测试结果id号")
    # 操作文件id号，唯一 允许为空
    file_id = models.IntegerField(null=True, verbose_name="文件id号")
    # 扩增任务id号，唯一 允许为空
    aug_id = models.IntegerField(null=True, verbose_name="扩增任务id号")
    # 任务状态,'ready'就绪,'running'运行中,'finish'完成
    task_state = models.CharField(max_length=64, verbose_name="文件状态")
    # 建立时间
    create_time = models.DateTimeField(default=timezone.now)
    # 开始运行时间
    start_time = models.DateTimeField(null=True)
    # 结束运行时间
    end_time = models.DateTimeField(null=True)

