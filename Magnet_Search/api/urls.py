from django.urls import path
from . import views
urlpatterns = [
    path('article_create/', views.ArticleAPIView.as_view(), name='article_create'),]
