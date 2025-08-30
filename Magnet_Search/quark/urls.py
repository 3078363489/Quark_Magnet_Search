from django.urls import path
from . import views
urlpatterns = [
    path('qurak_storage/', views.Quark_NetworkDisk.as_view(), name='qurak_storage'),
    path('qurak_Cache/', views.Quark_Cache.as_view(), name='Cache'),]