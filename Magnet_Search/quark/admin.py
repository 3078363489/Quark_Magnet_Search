from django.contrib import admin
from .models import quark_ck

@admin.register(quark_ck)
class QuarkCkAdmin(admin.ModelAdmin):
    # 禁用列表视图中的多行显示，改用单行编辑形式
    def has_add_permission(self, request):
        # 只允许存在一条记录
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    # 直接重定向到唯一对象的修改页面
    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse
        from django.shortcuts import redirect
        if self.model.objects.exists():
            obj = self.model.objects.first()
            return redirect(reverse('admin:%s_%s_change' % (
                self.model._meta.app_label,
                self.model._meta.model_name
            ), args=[obj.id]))
        return super().changelist_view(request, extra_context)

    # 修改编辑表单的显示字段
    fields = ('ck', 'fid')  # 只显示这两个字段