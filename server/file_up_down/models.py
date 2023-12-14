from django.db import models
from django.utils import timezone
# 文件模型
# class FileModel(models.Model):
#     # 文件名称
#     name = models.CharField(max_length=150)
#     # 文件保存路径
#     path = models.CharField(max_length=200)
#     # 上传时间
#     upload_time = models.DateTimeField(default=timezone.now)
#     # Create your models here.


class PhtotDataModel(models.Model):
    # 文件id号，唯一 允许为空
    file_id = models.IntegerField(null=True, verbose_name="文件id号")
    # 用户id号 允许为空
    user_id = models.IntegerField(null=True, verbose_name="用户id号")
    # 文件名称
    file_name = models.CharField(max_length=128, verbose_name="文件名称")
    # 文件类型, 2代表两车协同,3代表三车协同,...,n代表n车协同
    file_type = models.IntegerField(null=True, verbose_name="文件类型")
    # 文件状态, 'raw'代表未处理的原始数据,'augmented'代表已经扩增的数据
    file_state = models.CharField(max_length=64, verbose_name="文件状态")
    # 文件描述
    file_desc = models.CharField(max_length=256, verbose_name="文件描述")
    # 文件路径
    file_path = models.CharField(max_length=256, verbose_name="文件路径")
    # 上传时间
    upload_time = models.DateTimeField(default=timezone.now)