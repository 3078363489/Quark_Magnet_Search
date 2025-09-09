# installer/views.py
import json
import subprocess
import os
import shutil
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.models import User
from .models import InstallationStatus
import re

class InstallerView(TemplateView):
    template_name = 'installer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step'] = self.request.GET.get('step', '1')
        return context


class CheckEnvironmentView(View):
    def post(self, request):
        # 检查环境要求
        result = {
            'python': self._check_python(),
            'django': self._check_django(),
            'mysql': self._check_mysql(),
            'db_connection': False
        }

        return JsonResponse(result)

    def _check_python(self):
        import sys
        return sys.version_info >= (3, 6)

    def _check_django(self):
        from django import VERSION
        return VERSION >= (3, 0)

    def _check_mysql(self):
        try:
            import MySQLdb
            return True
        except ImportError:
            try:
                import pymysql
                pymysql.install_as_MySQLdb()
                return True
            except:
                return False


class TestDBConnectionView(View):
    def post(self, request):
        data = json.loads(request.body)

        # 测试数据库连接
        try:
            import MySQLdb
            conn = MySQLdb.connect(
                host=data.get('host', 'localhost'),
                port=int(data.get('port', 3306)),
                user=data.get('user', 'root'),
                passwd=data.get('password', ''),
                db=data.get('name', '')
            )
            conn.close()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class SaveDBConfigView(View):
    def post(self, request):
        data = json.loads(request.body)

        # 更新settings.py中的数据库配置
        settings_path = os.path.join(settings.BASE_DIR, 'Magnet_Search', 'settings.py')

        try:
            with open(settings_path, 'r',encoding='utf-8') as f:
                content = f.read()

            # 替换数据库配置
            new_db_config = f"""
DATABASES = {{
        'default': {{
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '{data.get('name', '')}',
            'USER': '{data.get('user', '')}',
            'PASSWORD': '{data.get('password', '')}',
            'HOST': '{data.get('host', 'localhost')}',
            'PORT': '{data.get('port', 3306)}',
        }}

"""

            # 查找并替换DATABASES配置
            import re
            pattern = r"DATABASES\s*=\s*\{[^}]+\}"
            content = re.sub(pattern, new_db_config, content)

            with open(settings_path, 'w',encoding='utf-8') as f:
                f.write(content)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class RunMigrationsView(View):
    def post(self, request):
        try:
            # 运行迁移命令
            result = subprocess.run([
                'python', os.path.join(settings.BASE_DIR, 'manage.py'), 'makemigrations'
            ], capture_output=True, text=True, cwd=settings.BASE_DIR)
            # 运行迁移命令
            result = subprocess.run([
                'python', os.path.join(settings.BASE_DIR, 'manage.py'), 'migrate'
            ], capture_output=True, text=True, cwd=settings.BASE_DIR)

            if result.returncode == 0:
                return JsonResponse({'success': True, 'output': result.stdout})
            else:
                return JsonResponse({'success': False, 'error': result.stderr})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class CreateAdminView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            # 使用子进程创建超级用户
            env = os.environ.copy()
            env['DJANGO_SUPERUSER_USERNAME'] = data.get('username')
            env['DJANGO_SUPERUSER_EMAIL'] = data.get('email')
            env['DJANGO_SUPERUSER_PASSWORD'] = data.get('password')

            result = subprocess.run([
                'python', os.path.join(settings.BASE_DIR, 'manage.py'), 'createsuperuser',
                '--noinput'
            ], env=env, capture_output=True, text=True, cwd=settings.BASE_DIR)

            if result.returncode == 0:
                InstallationStatus.objects.create(completed=True)
                return JsonResponse({'success': True})
            else:
                # 如果用户已存在，尝试非交互式创建
                try:
                    user = User.objects.create_superuser(
                        username=data.get('username'),
                        email=data.get('email'),
                        password=data.get('password')
                    )
                    InstallationStatus.objects.create(completed=True)
                    return JsonResponse({'success': True})
                except:
                    return JsonResponse({'success': False, 'error': result.stderr})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class CompleteInstallationView(View):
    def post(self, request):
        try:
            settings_path = os.path.join(settings.BASE_DIR, 'Magnet_Search', 'settings.py')
            # 读取settings.py内容
            with open(settings_path, 'r',encoding='utf-8') as f:
                content = f.read()
            # 从INSTALLED_APPS中移除'installer'
            content = self.remove_from_list(content, 'INSTALLED_APPS', 'installer')
            # 从MIDDLEWARE中移除'installer.middleware.InstallationMiddleware'
            content = self.remove_from_list(
                content,
                'MIDDLEWARE',
                'installer.middleware.InstallationMiddleware'
            )

            # 写回修改后的内容
            with open(settings_path, 'w',encoding='utf-8') as f:
                f.write(content)
            installer_path = os.path.join(settings.BASE_DIR, 'installer')

            if os.path.exists(installer_path):
                shutil.rmtree(installer_path)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def remove_from_list(self, content, setting_name, item_to_remove):
        """从设置列表中移除特定项"""
        # 匹配列表模式
        pattern = r"({}\s*=\s*\[)([^\]]*)(\])".format(setting_name)
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

        if match:
            prefix = match.group(1)
            list_content = match.group(2)
            suffix = match.group(3)

            # 移除项
            lines = list_content.split('\n')
            new_lines = []
            for line in lines:
                if item_to_remove not in line.strip(" ,'\""):
                    new_lines.append(line)

            new_list_content = '\n'.join(new_lines)
            new_content = content.replace(
                match.group(0),
                prefix + new_list_content + suffix
            )
            return new_content

        return content
