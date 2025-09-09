# installer/middleware.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings


class InstallationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 如果安装未完成且访问的不是安装页面，重定向到安装页面
        if not getattr(settings, 'INSTALLATION_COMPLETED', False) and \
                not request.path.startswith(reverse('installer:index')) and \
                not request.path.startswith('/static/') and \
                not request.path.startswith('/media/'):
            return HttpResponseRedirect(reverse('installer:index'))

        response = self.get_response(request)
        return response
