from django.db import models

# Create your models here.
class DatabaseModel(models.Model):
    # cid = models.CharField(max_length=64, verbose_name="")
    idx = models.IntegerField(null=True, verbose_name="userid")
    name = models.CharField(max_length=64, verbose_name="数据仓库名称")
    desc = models.CharField(max_length=64, verbose_name="数据仓库描述")
    path = models.CharField(max_length=256, verbose_name="数据仓库路径")
