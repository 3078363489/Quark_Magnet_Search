from django.db import models
# 在 quark 应用中
from article.models import Article
from django.conf import settings
import hashlib
# Create your models here.
class  quark_NetworkDisk(models.Model):
    link = models.URLField(max_length=500, verbose_name="链接", help_text="请输入链接")
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
    ck_hash = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Cookie哈希值",
        help_text="Cookie的SHA256哈希值"
    )
    ck = models.TextField(
        verbose_name="完整Cookie值",
        help_text="请输入完整的Cookie字符串"
    )
    fid = models.CharField(
        max_length=50,
        verbose_name="fid",
        help_text="请输入fid",
        default=settings.QUARK_CK_DEFAULT_FID
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ck_hash', 'fid')
        verbose_name = '夸克CK设置'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # 计算Cookie的哈希值
        self.ck_hash = hashlib.sha256(self.ck.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QuarkCK {self.fid} - {self.created_at}"
