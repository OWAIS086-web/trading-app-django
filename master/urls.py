
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from settings.views import user_settings, password_change_done
from users.views import chart_view, send_mass_message
from django.contrib.auth import views as auth_views
from admin_volt import views
from users.admin import UserProfileAdmin 
from admin_volt.views import chart, get_social_account_data
site_name = 'priority-gold-plus'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-', include('admin_volt.urls')),
    path('send_mass_message/', send_mass_message, name='send_mass_message'),
    path("", include("home.urls", namespace="home")),
    path("api/", include("api_modules.urls", namespace='api')),
    path("users/", include("users.urls", namespace="users")),
    path('password/reset/done/', auth_views.PasswordResetCompleteView.as_view(extra_context={'site_name': site_name}), name='password_reset_from_key_done'),
    path("users-settings/", user_settings, name="users-settings"),
    path("accounts/", include("allauth.urls")),
    path("portfolio/", include("portfolio.urls", namespace="portfolio")),
    path('user-settings/', include('settings.urls', namespace='settings')),
    path("modules/", include("modules.urls")),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-changed/', password_change_done, name='password_change_done'),
    path('charts/', views.user_chart_view, name='charts'),
    path('logged_in_users/', views.logged_in_users, name='logged_in_users'),
    path('chart/', views.chart, name='chart'),
    path('get_traffic_data/', views.get_traffic_data, name='get_traffic_data'),
    path('get_social_account_data/', get_social_account_data, name='get_social_account_data'),
   

]


# Add the media URL for development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)