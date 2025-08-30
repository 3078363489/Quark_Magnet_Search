from datetime import timedelta
from django.utils import timezone
import datetime
from .models import quark_NetworkDisk,quark_ck
from article.models import Article
from django.views import View
from . import quark as Quark
from django.http import JsonResponse  # 建议使用JsonResponse而不是HttpResponse返回JSON
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import time
# Create your views here.
from django.core.cache import cache

@method_decorator(csrf_exempt, name='dispatch')
class Quark_NetworkDisk(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Quark_link = data.get('Quark_link')
            network_id = data.get('network_id')

            # 验证参数
            if not Quark_link or not network_id:
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            # 获取文章对象
            try:

                article = Article.objects.get(id=network_id)
            except Article.DoesNotExist:

                return JsonResponse({'error': 'Article not found'}, status=404)

            if not article.state:
                return JsonResponse({'link': None, 'message': 'Article is not active'})

            # 检查是否有缓存（使用原子操作）
            cached_item = quark_NetworkDisk.objects.filter(network_id=article).first()
            if cached_item:
                # 更新访问时间
                cached_item.created_at = datetime.datetime.now()
                cached_item.save()
                return JsonResponse({'link': cached_item.link, 'cached': True})

            # 创建分布式锁的键
            lock_key = f'quark_lock_{network_id}'
            # 使用更可靠的锁机制，设置唯一标识符
            client_id = str(time.time()) + str(hash(request.META.get('REMOTE_ADDR', '')))

            # 尝试获取锁，设置较长的超时时间（例如60秒）
            acquired = cache.add(lock_key, client_id, timeout=60)

            if not acquired:
                # 检查锁是否由其他客户端持有
                current_lock_holder = cache.get(lock_key)
                if current_lock_holder != client_id:
                    # 等待其他请求完成，使用指数退避策略
                    retry_count = 0
                    max_retries = 15  # 最多等待约30秒

                    while retry_count < max_retries:
                        # 每次等待时间逐渐增加
                        sleep_time = 0.5 * (2 ** retry_count)
                        time.sleep(min(sleep_time, 5))  # 最多等待5秒一次

                        # 检查缓存是否已创建
                        cached_item = quark_NetworkDisk.objects.filter(network_id=article).first()
                        if cached_item:
                            return JsonResponse({'link': cached_item.link, 'cached': True})

                        # 检查锁是否已释放
                        if not cache.get(lock_key):
                            break

                        retry_count += 1

                    # 最终检查一次缓存
                    cached_item = quark_NetworkDisk.objects.filter(network_id=article).first()
                    if cached_item:
                        return JsonResponse({'link': cached_item.link, 'cached': True})
                    else:
                        return JsonResponse({'error': 'Operation timeout, please try again'}, status=408)

            try:
                # 再次检查缓存，防止在等待期间已有其他请求完成
                cached_item = quark_NetworkDisk.objects.filter(network_id=article).first()
                if cached_item:
                    return JsonResponse({'link': cached_item.link, 'cached': True})

                # 查找可用的夸克cookie
                quark_cookies = quark_ck.objects.all()
                if not quark_cookies.exists():
                    return JsonResponse({'link': Quark_link, 'cached': False, 'message': 'No cookie available'})

                # 获取第一个cookie和fid
                cookie = quark_cookies.first().ck
                fid = quark_cookies.first().fid

                # 使用夸克工具处理链接
                quark = Quark.QuarkTools(cookie)

                try:
                    result = quark.store_from_file(Quark_link, fid, False)
                    link, name_fid = result

                    # 创建缓存记录
                    quark_NetworkDisk.objects.create(
                        network_id=article,
                        link=link,
                        name_fid=name_fid
                    )
                    return JsonResponse({'link': link, 'cached': False})
                except Exception as e:
                    # 处理失败，更新文章状态
                    article.state = False
                    article.save()
                    # 记录错误日志
                    print(f"Failed to process Quark link: {str(e)}")
                    return JsonResponse({'link': None, 'message': f'Failed to process link: {str(e)}'})

            finally:
                # 只有锁的持有者才能释放锁
                if cache.get(lock_key) == client_id:
                    cache.delete(lock_key)

        except Exception as e:
            # 添加异常处理
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)


class Quark_Cache(View):
    def get(self, request):
        # 计算1小时前的时间
        one_hour_ago = timezone.now() - timedelta(hours=1)
        quark_cookies = quark_ck.objects.all()
        cookie = quark_cookies.first().ck
        # 获取所有创建时间超过1小时的记录
        expired_records = quark_NetworkDisk.objects.filter(created_at__lt=one_hour_ago)
        quark = Quark.QuarkTools(cookie)
        # 循环处理每条记录
        for quak_date in expired_records:
            # 可以在删除前执行其他操作，例如记录日志等
            print(f"正在删除记录 ID: {quak_date.id}, 创建时间: {quak_date.created_at}")
            quark.delete_from_file(quak_date.name_fid)
            # 删除记录
            quak_date.delete()

        return JsonResponse({"start": f"已删除 {expired_records.count()} 条过期记录"})



