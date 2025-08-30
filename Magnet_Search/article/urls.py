
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Article_indexView.as_view(), name='index'),
    path('resource/<int:article_id>/', views.Article_detailView.as_view(), name='detail'),
    path('increment-download/', views.increment_download, name='increment_download'),
    path('search/', views.ArticleSearchView.as_view(), name='search'),
    path('list/<int:category_id>/<int:page>', views.ArticlelistView.as_view(), name='list'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
]