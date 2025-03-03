from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
