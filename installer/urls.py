# installer/urls.py
from django.urls import path
from . import views

app_name = 'installer'

urlpatterns = [
    path('', views.InstallerView.as_view(), name='index'),
    path('check-environment/', views.CheckEnvironmentView.as_view(), name='check_environment'),
    path('test-db-connection/', views.TestDBConnectionView.as_view(), name='test_db_connection'),
    path('save-db-config/', views.SaveDBConfigView.as_view(), name='save_db_config'),
    path('run-migrations/', views.RunMigrationsView.as_view(), name='run_migrations'),
    path('create-admin/', views.CreateAdminView.as_view(), name='create_admin'),
    path('complete-installation/', views.CompleteInstallationView.as_view(), name='complete_installation'),
]