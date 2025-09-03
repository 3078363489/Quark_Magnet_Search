import re
from .models import SpiderVisit


class SpiderDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 定义搜索引擎爬虫的User-Agent正则表达式
        self.spider_patterns = {
            'baidu': r'baiduspider|Baiduspider',
            'google': r'googlebot|Googlebot',
            'bing': r'bingbot|Bingbot',
            'sogou': r'sogou.*spider|Sogou.*spider',
            '360': r'360spider|360Spider',
            'yandex': r'yandexbot|YandexBot',
            'duckduckgo': r'duckduckbot|DuckDuckBot',
        }

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        # 检查是否为搜索引擎爬虫
        search_engine = None
        for engine, pattern in self.spider_patterns.items():
            if re.search(pattern, user_agent, re.IGNORECASE):
                search_engine = engine
                break

        # 如果是爬虫，记录访问信息
        if search_engine:
            SpiderVisit.objects.create(
                ip_address=self.get_client_ip(request),
                user_agent=user_agent,
                search_engine=search_engine,
                path=request.path,
                referer=request.META.get('HTTP_REFERER', '')
            )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip