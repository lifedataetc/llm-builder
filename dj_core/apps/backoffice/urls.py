from django.urls import path
from apps.backoffice import views
from django.contrib import admin
from apps.backoffice.dash_apps import index, org_manager, pq_letters, settings_manager, user_manager
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
]