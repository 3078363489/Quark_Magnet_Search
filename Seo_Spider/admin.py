# admin.py
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.utils.html import format_html
from .models import SpiderVisit
import json

@admin.register(SpiderVisit)
class SpiderVisitAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['search_engine', 'ip_address', 'visit_time', 'path_short']
    list_filter = ['search_engine', 'visit_time']
    readonly_fields = ['ip_address', 'user_agent', 'visit_time', 'search_engine', 'path', 'referer']

    change_list_template = 'admin/spidervisit_change_list.html'

    def path_short(self, obj):
        return obj.path[:50] + '...' if len(obj.path) > 50 else obj.path

    path_short.short_description = '访问路径'

    def changelist_view(self, request, extra_context=None):
        # 准备图表数据
        stats = SpiderVisit.objects.values('search_engine').annotate(
            count=Count('id')
        ).order_by('-count')

        chart_data = {
            'labels': [self.model.SEARCH_ENGINES_DICT.get(stat['search_engine'], stat['search_engine'])
                       for stat in stats],
            'data': [stat['count'] for stat in stats],
            'backgroundColors': [
                '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                '#e74a3b', '#858796', '#f8f9fc', '#5a5c69'
            ]
        }

        extra_context = extra_context or {}
        extra_context['chart_data'] = json.dumps(chart_data)

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart_data/', self.admin_site.admin_view(self.chart_data), name='seo_tracker_chart_data'),
        ]
        return custom_urls + urls

    def chart_data(self, request):
        # 提供图表数据的API端点
        stats = SpiderVisit.objects.values('search_engine').annotate(
            count=Count('id')
        ).order_by('-count')

        data = {
            'labels': [self.model.SEARCH_ENGINES_DICT.get(stat['search_engine'], stat['search_engine'])
                       for stat in stats],
            'datasets': [{
                'data': [stat['count'] for stat in stats],
                'backgroundColor': [
                    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                    '#e74a3b', '#858796', '#f8f9fc', '#5a5c69'
                ]
            }]
        }

        return JsonResponse(data)