from django.db import models
# 在 quark 应用中
from article.models import Article
from django.conf import settings
# Create your models here.
class  quark_NetworkDisk(models.Model):
    link = models.URLField(max_length=2000, verbose_name="链接", help_text="请输入链接")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="添加时间",
        help_text="资源添加的日期和时间",
        db_index=True  # 添加索引加速排序
    )
    name_fid = models.CharField(
        max_length=100,
        verbose_name="文件名id",
        help_text="请输入文件名id", )
    network_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="网络硬盘资源",
                                   help_text="请选择网络硬盘资源")


class quark_ck(models.Model):
    ck = models.CharField(
        max_length=settings.MAX_CK_LENGTH,  # 使用全局设置
        verbose_name="ck",
        help_text="请输入ck"
    )
    fid = models.CharField(
        max_length=100,
        verbose_name="fid",
        help_text="请输入fid",
        default=settings.QUARK_CK_DEFAULT_FID  # 使用全局默认值
    )
    class Meta:
        unique_together = ('ck', 'fid')  # 设置联合唯一索引
        # Create your models here.
        verbose_name = '夸克ck设置'
        verbose_name_plural = verbose_name