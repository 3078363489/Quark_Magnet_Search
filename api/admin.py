from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Key


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('key', 'name')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    actions = ['activate_keys', 'deactivate_keys']

    fieldsets = (
        (None, {
            'fields': ('key', 'name', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def activate_keys(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, ngettext(
            '%d 个密钥已被激活。',
            '%d 个密钥已被激活。',
            updated,
        ) % updated, messages.SUCCESS)

    activate_keys.short_description = "激活所选密钥"

    def deactivate_keys(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, ngettext(
            '%d 个密钥已被停用。',
            '%d 个密钥已被停用。',
            updated,
        ) % updated, messages.SUCCESS)

    deactivate_keys.short_description = "停用所选密钥"

    # 可选：自动生成密钥
    def save_model(self, request, obj, form, change):
        if not obj.key:  # 如果没有提供密钥，自动生成
            import secrets
            obj.key = secrets.token_urlsafe(32)
        super().save_model(request, obj, form, change)