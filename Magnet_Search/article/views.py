from django.http import HttpResponse
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from django.views import View
from .models import Article,Article_type,Downloads,SiteConfig
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.http import JsonResponse
from django.db.models import Q, F
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
class Article_indexView(View):
    def get(self,request):
        types = Article_type.objects.prefetch_related(
            Prefetch('article_set', queryset=Article.objects.all())
        ).all()
        articles = {
            t.type: {
                'icon': t.Font_Awesome_Web,  # 图标类名
                'type_id':t.id,
                'articles': t.article_set.all().order_by('-Create_date')[:5]  # 文章列表
                    }
            for t in types
        }
        return render(request,'index.html',{'articles':articles})





# @method_decorator(cache_page(60 * 15), name='dispatch')  # 缓存15分钟
class Article_detailView(View):
    def get(self, request, article_id):
        article = get_object_or_404(
            Article.objects.select_related('author', 'type'),
            id=article_id
        )
        related_articles = Article.objects.filter(
            type=article.type
        ).exclude(id=article_id).order_by('-Create_date')[:5]
        # 更新访问计数（绕过缓存）
        Article.objects.filter(id=article_id).update(
            view_count=models.F('view_count') + 1
        )

        return render(request, 'detail.html', {
            'article': article,
            'article_type': article.type,
            'related_articles':related_articles

        })


# views.py (修正)

class ArticleSearchView(View):
    def get(self, request):
        # 获取搜索词
        search_term = request.GET.get('q', '').strip()

        # 构建基础查询集
        if search_term:
            # 使用 MySQL 兼容的搜索
            results = Article.objects.filter(
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term) |
                Q(tags__tag__icontains=search_term)
            ).distinct().order_by('-Create_date')
        else:
            results = Article.objects.all().order_by('-Create_date')

        # 优化查询性能
        results = results.prefetch_related('tags').select_related('type')
        total_count = results.count()
        # 创建分页器
        paginator = Paginator(results,5)  # 每页10篇文章
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # 如果页码不是整数，显示第一页
            page_obj = paginator.page(1)
        except EmptyPage:
            # 如果页码超出范围，显示最后一页
            page_obj = paginator.page(paginator.num_pages)

        # 计算页码范围
        page_range = self.get_page_range(page_obj, paginator)

        # 构建查询参数
        query_params = {}
        if search_term:
            query_params['q'] = search_term

        # SEO优化元素
        context = {
            'article_count':total_count,
            'page_obj': page_obj,
            'search_term': search_term,
            'page_range': page_range,
            'query_params': query_params,
            'page_title': f"搜索: {search_term}" if search_term else "所有文章",
            'meta_description': f"包含'{search_term}'的相关文章搜索结果" if search_term else "最新文章列表",
        }
        return render(request, 'Search.html', context)

    def get_page_range(self, page_obj, paginator, delta=2):
        """生成智能页码范围，只显示当前页附近的页码"""
        current_page = page_obj.number
        total_pages = paginator.num_pages

        # 计算页码范围
        start = max(1, current_page - delta)
        end = min(total_pages, current_page + delta) + 1

        # 添加首尾页
        page_range = []
        if start > 1:
            page_range.append(1)
            if start > 2:
                page_range.append(None)  # 表示省略号

        page_range.extend(range(start, end))

        if end <= total_pages:
            if end < total_pages:
                page_range.append(None)  # 表示省略号
            page_range.append(total_pages)

        return page_range


class ArticlelistView(View):
    def get(self, request, category_id, page=1):  # 添加page参数，默认为1
        # 获取分类对象
        category = get_object_or_404(Article_type, id=category_id)

        # 获取文章列表
        results = Article.objects.filter(type=category_id).distinct().order_by('-Create_date')
        total_count = results.count()

        # 创建分页器
        paginator = Paginator(results, 5)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # 计算页码范围
        page_range = self.get_page_range(page_obj, paginator)

        context = {
            'article_count': total_count,
            'page_obj': page_obj,
            'page_range': page_range,
            'category': category,
            'current_page': page,  # 添加当前页码
        }
        return render(request, 'list.html', context)

    def get_page_range(self, page_obj, paginator, delta=2):
        """生成智能页码范围，只显示当前页附近的页码"""
        current_page = page_obj.number
        total_pages = paginator.num_pages

        # 计算页码范围
        start = max(1, current_page - delta)
        end = min(total_pages, current_page + delta) + 1

        # 添加首尾页
        page_range = []
        if start > 1:
            page_range.append(1)
            if start > 2:
                page_range.append(None)  # 表示省略号

        page_range.extend(range(start, end))

        if end <= total_pages:
            if end < total_pages:
                page_range.append(None)  # 表示省略号
            page_range.append(total_pages)

        return page_range

def increment_download(request):
    """增加下载计数 (API端点)"""
    # 获取或创建统计记录（放在开头确保stats对象存在）
    stats, created = Downloads.objects.get_or_create(
        defaults={
            'Weekly_Downloads': 0,
            'Total_Downloads': 0,
            'last_reset': timezone.now().date()
        }
    )

    # 检查是否需要重置（距离上次重置是否超过7天）
    if timezone.now().date() >= stats.last_reset + timedelta(days=7):
        # 调用模型的reset方法（如果有）或直接重置
        if hasattr(stats, 'reset_weekly_downloads'):
            stats.reset_weekly_downloads()
        else:
            stats.Weekly_Downloads = 0
            stats.last_reset = timezone.now().date()

    # 增加下载量
    stats.Weekly_Downloads += 1
    stats.Total_Downloads += 1
    stats.save()

    return JsonResponse({
        'weekly': stats.Weekly_Downloads,
        'total': stats.Total_Downloads,
        'last_reset': stats.last_reset.strftime('%Y-%m-%d')
    })


# views.py
from django.http import HttpResponse
from django.urls import reverse
from .models import Article, SiteConfig
from datetime import datetime
from django.utils.timezone import get_current_timezone


def sitemap_xml(request):
    """手动生成sitemap.xml"""
    # 获取配置
    config = SiteConfig.get_config()

    # 获取所有网盘有效的文章
    articles = Article.objects.filter(
        state=True
    ).order_by('-Update_date', '-Create_date')

    # 应用数量限制
    if config.sitemap_max_articles:
        articles = articles[:config.sitemap_max_articles]

    # 构建XML内容
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # 添加首页
    xml_content.append('  <url>')
    xml_content.append(f'    <loc>{config.site_domain.rstrip("/")}</loc>')
    xml_content.append('    <changefreq>daily</changefreq>')
    xml_content.append('    <priority>1.0</priority>')
    xml_content.append('  </url>')

    # 添加文章页面
    for article in articles:
        # 构建完整的URL
        article_path = reverse('detail', kwargs={'article_id': article.id})
        article_url = f"{config.site_domain.rstrip('/')}{article_path}"

        # 格式化最后修改时间
        lastmod = article.Update_date.astimezone(get_current_timezone()).strftime('%Y-%m-%d')

        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{article_url}</loc>')
        xml_content.append(f'    <lastmod>{lastmod}</lastmod>')
        xml_content.append('    <changefreq>weekly</changefreq>')
        xml_content.append('    <priority>0.8</priority>')
        xml_content.append('  </url>')

    xml_content.append('</urlset>')

    # 返回XML响应
    return HttpResponse('\n'.join(xml_content), content_type='application/xml')