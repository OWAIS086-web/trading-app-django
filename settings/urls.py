# user_settings/urls.py
from django.urls import path
from .views import user_settings, change_password
from .views import notification_settings
from . import views
app_name = 'settings'

urlpatterns = [
    path('users-settings/', user_settings, name='users-settings'),
    path('change-password/', change_password, name='change_password'),
    path('notification-settings', views.notification_settings, name='notification_settings'),
    
]
