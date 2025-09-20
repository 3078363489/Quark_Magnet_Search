
from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.conf import settings
#设置redis页面缓存
def cachetime(timeout):
    def decorator(view):
        if hasattr(settings, 'CACHE'):
            return cache_page(timeout)(view)
        return view
    return decorator
urlpatterns = [
    path('', views.Article_indexView.as_view(), name='index'),
    path('resource/<int:article_id>/', views.Article_detailView.as_view(), name='detail'),
    path('increment-download/', views.increment_download, name='increment_download'),
    path('search/', cachetime(60 * 60)(views.ArticleSearchView.as_view()), name='search'),
    path('list/<int:category_id>/<int:page>', cachetime(60 * 60)(views.ArticlelistView.as_view()), name='list'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),

]
