from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/opportunities/', views.get_opportunities, name='api-opportunities'),
    path('update-config/', views.update_config, name='update-config'),
    path('toggle-bot/', views.toggle_bot, name='toggle-bot'),
]