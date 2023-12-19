from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = "users"
urlpatterns = [
    # path("~signup/", SignUpView.as_view(), name="signup"),
    path("sign-up/", views.sign_up, name="sign_up"),
    # path("signup/", views.user_registration_view, name="signup"),
    path("staff-signup/", views.staff_registration_view, name="staff_signup"),
    path("admin-signup/", views.admin_registration_view, name="admin_signup"),
    path("user-profile/", views.profile_view, name="user_profile"),
    path("edit-user-profile/", views.edit_profile, name="edit_profile"),
    path("~redirect/", view=views.user_redirect_view, name="redirect"),
    path("~update/", view=views.user_update_view, name="update"),
    path("<str:username>/", view=views.user_detail_view, name="detail"),
    # path("<str:username>/", view=portfolio , name="portfolio"),
    path('otp-verification/<str:uidb64>/<str:token>/', views.opt_verification_view.as_view(), name='user_otp_verification'),
    path('resend_otp/<str:uidb64>/<str:token>/', view=views.resend_otp, name='user_resend_otp'),
    path("jbplaccountsetting/", views.settings_view, name="accountsetting"),
    path('portfolio/',views.portfolio,name='portfolio'),
    path('portfolio-main/',views.portfolio_main,name='portfolio_main'),
    # path('view-profile/',views.view_profile_view,name='view_profile'),
    path('add-metal-form/',views.add_metal_form,name='add_metal_form'),

]
    
    
    

