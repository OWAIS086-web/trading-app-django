from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # Import the obtain_auth_token view

from . import views, viewsets
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView
)


router = DefaultRouter()
app_name = 'users'

urlpatterns = [
    path("", include(router.urls)),
    # path('send-app-link/', views.SendEmailInvitationAPIView.as_view()),
    # path('app-store-links/', views.AppStoreLinkAPIView.as_view()),
    # path('db/', views.DBUrlTest.as_view()),
    # path("user-signup/", views.UserAPIView.as_view(), name="user_signup"),
        # path("accounts/", include("allauth.urls")),
    
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('rest-auth/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('logout/', LogoutView.as_view(), name='rest_logout'),
    # path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    
    path('upload/media-file/', views.MediaFilesUploadAPIView.as_view(), name='media_files_upload'),
    path('token/', obtain_auth_token, name='obtain-token'),  # URL to obtain the token
    path('user-profile/', views.AccountAuthProfileDetailAPIView.as_view(), name='user_profile'),
    path('accounts/password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset_api'),
    path('reset-password/', views.CustomPasswordResetView.as_view(), name='reset_password'),
    path('user-profile/', views.AccountAuthProfileDetailAPIView.as_view(), name='user_profile'),
    path('update-user-profile/', views.UpdateUserProfileAPIView.as_view(), name='update_profile'),
    path('registration/verify-otp/', views.VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('registration/resend-otp/', views.ResendOTPVerificationAPIView.as_view(), name="resend_otp"),
    path('delete-account/', views.AccountDeleteAPIView.as_view(), name='delete_account'),
    path('registration/user/', views.UserRegistrationAPIView.as_view(), name='user_registration'),
    path('login/token/', views.AccountTokenLoginAPIView.as_view(), name='token_login'),
    path('verify-email-exists/', views.VerifyEmailExistAPIView.as_view(), name='verify_email_exists')
]