# models.py
from django.db import models


class SpiderVisit(models.Model):  # 修改类名为SpiderVisit
    SEARCH_ENGINES = (
        ('baidu', '百度'),
        ('google', '谷歌'),
        ('bing', '必应'),
        ('sogou', '搜狗'),
        ('360', '360搜索'),
        ('yandex', 'Yandex'),
        ('duckduckgo', 'DuckDuckGo'),
        ('other', '其他爬虫'),
    )
    SEARCH_ENGINES_DICT = dict(SEARCH_ENGINES)  # 添加这个字典

    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(verbose_name='User Agent')
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')
    search_engine = models.CharField(max_length=20, choices=SEARCH_ENGINES, verbose_name='搜索引擎')
    path = models.CharField(max_length=500, verbose_name='访问路径')
    referer = models.URLField(blank=True, null=True, verbose_name='来源页面')

    class Meta:
        verbose_name = '爬虫访问记录'
        verbose_name_plural = '爬虫访问记录'
        ordering = ['-visit_time']

    def __str__(self):
        return f"{self.get_search_engine_display()} - {self.visit_time.strftime('%Y-%m-%d %H:%M')}"
