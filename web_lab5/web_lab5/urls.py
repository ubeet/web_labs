"""
URL configuration for web_lab5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('admin-mode/', views.set_admin_mode, name='set_admin_mode'),
    path('logout-admin/', views.logout_admin_mode, name='logout_admin_mode'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('news/<int:id>/edit/', views.news_edit, name='news_edit'),
    path('news/<int:id>/delete/', views.news_delete, name='news_delete'),
]
