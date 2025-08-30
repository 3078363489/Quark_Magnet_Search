from django.db import models


class Key(models.Model):
    key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, help_text="密钥描述或名称")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class meta:
        verbose_name = "采集密钥"
        verbose_name_plural = verbose_name
    def __str__(self):
        return f"{self.name} ({self.key})" if self.name else self.key