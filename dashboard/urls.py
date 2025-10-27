from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.slideshow_view, name='slideshow'),
    path('api/config/', views.get_dashboards_config, name='api_config'),
]
