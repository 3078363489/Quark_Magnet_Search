from django.db import models
from django.contrib.auth import models as user
from django.utils import timezone
from django.core.validators import URLValidator
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200,verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    view_count = models.IntegerField(default=0,verbose_name="阅读量")
    author = models.ForeignKey(user.User,on_delete=models.CASCADE,verbose_name="作者")
    tags = models.ManyToManyField('Article_tag', verbose_name="标签")
    Create_date = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    Update_date = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    type = models.ForeignKey('Article_type',on_delete=models.CASCADE,verbose_name="分类")
    link = models.CharField(max_length=200,verbose_name="夸克网盘链接")
    state= models.BooleanField(default=True,verbose_name="网盘状态")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
class Article_type(models.Model):
    type = models.CharField(max_length=20,verbose_name="分类")
    Font_Awesome_Web= models.CharField(max_length=20,verbose_name="图标",default='None')
    def __str__(self):
        return self.type
    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
class Article_tag(models.Model):
    tag = models.CharField(max_length=20,verbose_name="标签")
    def __str__(self):
        return self.tag
    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name


class Site_Information(models.Model):
    singleton = models.BooleanField(default=True, editable=False, unique=True)
    Site_title = models.CharField(max_length=100, verbose_name="网站标题")
    Site_title_wei = models.CharField(max_length=100, verbose_name="副标题", blank=True)
    description = models.TextField(verbose_name="网站描述", blank=True)
    keywords = models.CharField(max_length=200, verbose_name="关键词", blank=True)
    for_the_record = models.CharField(max_length=30,verbose_name='备案号',blank=True)
    analytics_code = models.TextField(verbose_name="分析代码", blank=True)  # 新增
    footer_content = models.TextField(verbose_name="页脚内容", blank=True)  # 新增

    @classmethod
    def get_singleton(cls):
        obj, created = cls.objects.get_or_create(singleton=True)
        return obj

    def __str__(self):
        return self.Site_title

    class Meta:
        verbose_name = '网站信息'
        verbose_name_plural = verbose_name
class Friendship_Link(models.Model):
    name = models.CharField(max_length=200,verbose_name="网站名称")
    url = models.CharField(max_length=200,verbose_name="网站链接")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


class Downloads(models.Model):
    Weekly_Downloads = models.IntegerField(default=0, verbose_name="周下载量")
    Total_Downloads = models.IntegerField(default=0, verbose_name="总下载量")
    last_reset = models.DateField(auto_now=True, verbose_name="上次重置时间")

    class Meta:
        verbose_name = "下载量统计"
        verbose_name_plural = "下载量统计"

    def __str__(self):
        return f"下载统计 (周下载: {self.Weekly_Downloads}, 总下载: {self.Total_Downloads})"

    def reset_weekly_downloads(self):
        """重置周下载量并更新最后重置时间"""
        self.Weekly_Downloads = 0
        self.last_reset = timezone.now().date()
        self.save()


class SiteConfig(models.Model):
    """网站配置模型"""
    site_domain = models.CharField(
        max_length=200,
        default='https://example.com',
        validators=[URLValidator()],
        verbose_name="网站域名",
        help_text="用于生成sitemap的完整域名，例如: https://yourdomain.com"
    )
    sitemap_max_articles = models.PositiveIntegerField(
        default=1000,
        verbose_name="网站地图最大文章数量",
        help_text="设置网站地图中最多显示的文章数量"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "网站地图配置"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # 确保域名以/结尾
        if not self.site_domain.endswith('/'):
            self.site_domain = self.site_domain + '/'
        # 确保只有一个配置实例
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        """获取配置实例"""
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls.objects.create(
                site_domain='https://example.com/',
                sitemap_max_articles=1000
            )