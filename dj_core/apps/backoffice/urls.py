from django.urls import path
from apps.backoffice import views
from django.contrib import admin
from apps.backoffice.dash_apps import index, org_manager, settings_manager, user_manager, vectorizer

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('user_manager/', views.user_manager, name='user manager'),
    path('org_manager/', views.org_manager, name='org manager'),
    path('vec_db/', views.vectorizer, name='vectorizer'),

]