
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Article_tag, Friendship_Link,SiteConfig,Article_type, Site_Information


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_domain', 'sitemap_max_articles', 'updated_at')
    fields = ('site_domain', 'sitemap_max_articles')

    def has_add_permission(self, request):
        # 只允许有一个配置实例
        return not SiteConfig.objects.exists()


class ArticleForm(forms.ModelForm):
    list_per_page = 20
    tags_input = forms.CharField(
        label='标签',
        required=False,
        help_text='输入逗号分隔的标签（例如: 书籍,虚幻,编程）。已存在的标签会自动关联，不存在的标签会被创建。'
    )

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('tags',)  # 排除原生多对多字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # 编辑时显示已有标签（逗号分隔）
            self.fields['tags_input'].initial = ", ".join(
                [tag.tag for tag in self.instance.tags.all()]
            )

    def save(self, commit=True):
        # 保存文章实例但不提交多对多关系
        article = super().save(commit=False)

        # 获取标签输入
        tags_input = self.cleaned_data.get('tags_input', '')

        # 必须先保存文章获取ID
        article.save()  # 关键：先保存文章获取ID

        # 处理标签关联（确保文章已有ID）
        self.process_tags(article, tags_input)

        # 如果commit=False，需要额外处理
        if not commit:
            # 返回文章实例但不保存多对多关系
            return article

        # 确保所有关系已保存
        self.save_m2m()
        return article

    def save_m2m(self):
        """处理多对多关系保存（当commit=False时）"""
        # 不需要调用super()，因为我们手动处理了标签关系
        pass

    def process_tags(self, article, tags_input):
        """处理标签关联逻辑"""
        if not tags_input:
            # 清空标签（当输入为空时）
            article.tags.clear()
            return

        # 清理并分割标签
        tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        # 清空现有标签关联
        article.tags.clear()

        # 创建或获取标签对象并关联
        for tag_name in tags_list:
            tag, created = Article_tag.objects.get_or_create(tag=tag_name)
            article.tags.add(tag)


class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 20
    form = ArticleForm

    list_display = [
        'title',
        'get_article_type',
        'get_tags_display',
        'get_font_awesome',
        'content_preview',
        'get_created_date',
        'get_link_display',
        'state'  # 添加网盘状态字段
    ]
    list_filter = ('type', 'tags', 'Create_date', 'state')  # 添加状态过滤器
    search_fields = ['title', 'content', 'type__type']
    readonly_fields = ('Create_date', 'Update_date')
    list_editable = ['state']  # 允许直接在列表页编辑状态

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'author', 'link', 'state')  # 添加状态字段
        }),
        ('分类与标签', {
            'fields': ('type', 'tags_input')
        }),
        ('时间信息', {
            'fields': ('Create_date', 'Update_date'),
            'classes': ('collapse',)
        }),
    )

    # 保持原有的自定义方法不变
    def get_article_type(self, obj):
        return obj.type.type if obj.type else '-'

    get_article_type.short_description = '分类'
    get_article_type.admin_order_field = 'type__type'

    def get_tags_display(self, obj):
        return ", ".join([tag.tag for tag in obj.tags.all()]) or '-'

    get_tags_display.short_description = '标签'

    def get_font_awesome(self, obj):
        return obj.type.Font_Awesome_Web if obj.type else '-'

    get_font_awesome.short_description = '图标'

    def content_preview(self, obj):
        preview = obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, preview)

    content_preview.short_description = '内容预览'

    def get_created_date(self, obj):
        return obj.Create_date.strftime('%Y-%m-%d %H:%M')

    get_created_date.short_description = '创建时间'
    get_created_date.admin_order_field = 'Create_date'

    def get_link_display(self, obj):
        if obj.link:
            # 根据状态显示不同的样式
            if obj.state:
                return format_html('<a href="{}" target="_blank" style="color: green;">✓ 查看链接</a>', obj.link)
            else:
                return format_html('<a href="{}" target="_blank" style="color: red;">✗ 查看链接</a>', obj.link)
        return '-'

    get_link_display.short_description = '网盘链接'



# 文章类型管理
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'Font_Awesome_Web')
    search_fields = ('type',)


# 文章标签管理
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)


# 然后优化管理类
@admin.register(Site_Information)
class SiteInformationAdmin(admin.ModelAdmin):
    # 隐藏单例字段
    exclude = ('singleton',)

    # 表单字段分组（只包含实际存在的字段）
    fieldsets = (
        ('基本信息', {
            'fields': ('Site_title', 'Site_title_wei','for_the_record'),
            'description': '网站的基本标题信息'
        }),
        ('SEO设置', {
            'fields': ('description', 'keywords'),
            'description': '这些信息将用于搜索引擎优化(SEO)'
        }),
        ('高级设置', {
            'fields': ('analytics_code', 'footer_content'),
            'classes': ('collapse',),  # 可折叠
            'description': '网站分析和页脚内容'
        }),
    )

    # 单例模式控制
    def has_add_permission(self, request):
        """禁止添加新记录（通过单例方法创建）"""
        return False

    def has_delete_permission(self, request, obj=None):
        """禁止删除记录"""
        return False

    def changelist_view(self, request, extra_context=None):
        """自动重定向到编辑页面"""
        # 获取单例实例
        obj = Site_Information.get_singleton()
        return redirect(
            reverse('admin:%s_%s_change' % (
                obj._meta.app_label,
                obj._meta.model_name
            ), args=[obj.id])
        )

    def save_model(self, request, obj, form, change):
        """保存模型并添加成功消息"""
        super().save_model(request, obj, form, change)
        messages.success(request, '网站信息已成功更新！')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """自定义表单视图"""
        extra_context = extra_context or {}
        extra_context['title'] = '网站全局设置'

        # 添加帮助文本
        help_texts = {
            'analytics_code': '例如：Google Analytics 或百度统计代码',
            'footer_content': '支持HTML格式的页脚内容'
        }
        extra_context['help_texts'] = help_texts

        return super().changeform_view(request, object_id, form_url, extra_context)

    # 添加表单字段的额外帮助文本
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        help_texts = {
            'analytics_code': '在此处粘贴您的网站分析跟踪代码',
            'footer_content': '支持HTML格式的内容，将显示在网站页脚'
        }
        if db_field.name in help_texts:
            field.help_text = help_texts[db_field.name]
        return field


# 注册模型
admin.site.register(Article, ArticleAdmin)
admin.site.register(Article_type, ArticleTypeAdmin)  # 添加管理类
admin.site.register(Article_tag, ArticleTagAdmin)  # 注册标签模型
@admin.register(Friendship_Link)
class Friendship_Link_Admin(admin.ModelAdmin):
    list_display = [
        'name',
        'url',
    ]
