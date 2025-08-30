from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
import json
import re
from article.models import Article, Article_type, Article_tag
from .models import Key
from django.contrib.auth.models import User
from urllib.parse import unquote, parse_qs

@method_decorator(csrf_exempt, name='dispatch')
class ArticleAPIView(View):
    def _validate_api_key(self, request):
        """
        验证API密钥
        """
        # 从请求头获取API密钥
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return False, JsonResponse(
                {'error': 'API key required'},
                status=401
            )

        # 检查密钥是否存在且有效
        try:
            key_obj = Key.objects.get(key=api_key)
            if not key_obj.is_active:
                return False, JsonResponse(
                    {'error': 'API key is not active'},
                    status=401
                )
            return True, None
        except Key.DoesNotExist:
            return False, JsonResponse(
                {'error': 'Invalid API key'},
                status=401
            )

    def _parse_request_body(self, request):
        """
        解析请求体，支持JSON和URL编码格式
        """
        try:
            # 尝试UTF-8解码
            body_str = request.body.decode('utf-8')
        except UnicodeDecodeError:
            try:
                # 尝试GBK解码
                body_str = request.body.decode('gbk')
            except UnicodeDecodeError:
                return None, JsonResponse(
                    {'error': 'Unable to decode request body'},
                    status=400
                )

        # 记录原始请求体以便调试
        print(f"原始请求体: {body_str[:500]}...")  # 只打印前500个字符

        # 首先尝试解析为JSON
        try:
            parsed_data = json.loads(body_str)
            return parsed_data, None
        except json.JSONDecodeError:
            # 如果不是JSON，尝试解析为URL编码格式
            try:
                parsed_data = parse_qs(body_str)
                # 将列表值转换为单个值
                decoded_data = {}
                for key, value in parsed_data.items():
                    if isinstance(value, list) and len(value) == 1:
                        decoded_data[key] = unquote(value[0])
                    else:
                        decoded_data[key] = [unquote(v) for v in value]
                return decoded_data, None
            except Exception as e:
                return None, JsonResponse(
                    {'error': f'Unable to parse request body: {str(e)}'},
                    status=400
                )

    def post(self, request):
        # 验证API密钥
        is_valid, error_response = self._validate_api_key(request)
        if not is_valid:
            return error_response

        # 解析请求体
        data, error_response = self._parse_request_body(request)
        if error_response:
            return error_response

        # 提取数据
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author')
        article_type_id = data.get('type')
        link = data.get('link')
        tags_input = data.get('tags', '')  # 接收字符串而不是列表

        # 验证必填字段
        required_fields = ['title', 'content', 'author', 'type', 'link']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {'error': f'Missing required field: {field}'},
                    status=400
                )

        # 创建文章
        try:
            # 获取外键对象
            author = User.objects.get(id=author_id)
            article_type = Article_type.objects.get(id=article_type_id)

            # 创建文章实例
            article = Article.objects.create(
                title=title,
                content=content,
                author=author,
                type=article_type,
                link=link
            )

            # 处理标签 - 支持逗号分隔的字符串
            if tags_input:
                # 分割标签字符串
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

                # 处理每个标签
                for tag_name in tag_names:
                    # 获取或创建标签
                    tag, created = Article_tag.objects.get_or_create(tag=tag_name)
                    # 添加到文章
                    article.tags.add(tag)

            return JsonResponse({
                'message': 'Article created successfully',
                'id': article.id
            }, status=201)
        except User.DoesNotExist:
            return JsonResponse(
                {'error': 'Author not found'},
                status=400
            )
        except Article_type.DoesNotExist:
            return JsonResponse(
                {'error': 'Article type not found'},
                status=400
            )
        except ValidationError as e:
            return JsonResponse(
                {'error': str(e)},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': f'Internal server error: {str(e)}'},
                status=500
            )

    def get(self, request, article_id=None):
        # 验证API密钥
        is_valid, error_response = self._validate_api_key(request)
        if not is_valid:
            return error_response

        # 获取单篇文章或多篇文章
        if article_id:
            try:
                article = Article.objects.get(id=article_id)
                # 获取标签名称列表而不是ID
                tag_names = list(article.tags.values_list('tag', flat=True))

                return JsonResponse({
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'author': article.author.id,
                    'type': article.type.id,
                    'link': article.link,
                    'tags': tag_names,  # 返回标签名称列表
                    'view_count': article.view_count,
                    'created_date': article.Create_date.isoformat(),
                    'updated_date': article.Update_date.isoformat(),
                    'state': article.state
                })
            except Article.DoesNotExist:
                return JsonResponse(
                    {'error': 'Article not found'},
                    status=404
                )
        else:
            # 返回文章列表
            articles = Article.objects.all().values(
                'id', 'title', 'author__username', 'type__name', 'Create_date', 'view_count'
            )
            articles_list = list(articles)
            for article in articles_list:
                article['Create_date'] = article['Create_date'].isoformat()

            return JsonResponse(articles_list, safe=False)