from django.db import models
from django.utils import timezone

# 扩增配置
class AugConfig(models.Model):
    # 任务id号，唯一 允许为空
    config_id = models.IntegerField(null=True, verbose_name="任务id号")
    # 是否使用默认参数标志，true代表参数默认，false代表使用用户输入的参数
    default_flag = models.BooleanField()
    # 扩增类型，'brightness'亮度,'vague'模糊,'noise'椒盐噪声
    aug_type = models.CharField(max_length=64, verbose_name="扩增类型")
    # 扩增强度，max_digits 总位数(不包括小数点和符号),decimal_places 小数位数、、max_digits=6, decimal_places=2
    aug_para = models.IntegerField(null=True, verbose_name="扩增参数")

    # 中心车辆id号
    ego_car_id = models.IntegerField(default=0,null=True, verbose_name="中心车辆id号")
    # 是否分别对不同车辆数据进行扩增
    separate_flag = models.BooleanField(default=False)


# 扩增任务
class AugTask(models.Model):
    # 任务id号，唯一 允许为空
    task_id = models.IntegerField(null=True, verbose_name="任务id号")
    # 任务名称
    task_name = models.CharField(max_length=256, verbose_name="任务名称")
    # 用户id号 允许为空
    user_id = models.IntegerField(null=True, verbose_name="用户id号")
    # 操作文件id号，唯一 允许为空
    raw_file_id = models.IntegerField(null=True, verbose_name="文件id号")
    # 扩增完成文件id号，唯一 允许为空
    aug_file_id = models.IntegerField(null=True, verbose_name="扩增完成文件id号")
    # 任务状态,'ready'就绪,'running'运行中,'finish'完成
    task_state = models.CharField(max_length=64, verbose_name="文件状态")
    # 扩增配置id号，唯一 允许为空
    config_id = models.IntegerField(null=True, verbose_name="扩增配置id号")
    # 建立时间
    create_time = models.DateTimeField(default=timezone.now)
    # 开始运行时间
    start_time = models.DateTimeField(null=True)
    # 结束运行时间
    end_time = models.DateTimeField(null=True)