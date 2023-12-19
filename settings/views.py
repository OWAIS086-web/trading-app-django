# user_settings/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ChangePasswordForm, NotificationSettingsForm
from .models import UserNotification
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def user_settings(request):
    return render(request, 'settings/setting.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('settings:settings')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'settings/setting.html', {'form': form})

# @login_required
# def notification_settings(request):
#     user_notification, created = UserNotification.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = NotificationSettingsForm(request.POST, instance=user_notification)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Notification settings updated.')
#             return redirect('settings:users-settings')
#     else:
#         form = NotificationSettingsForm(instance=user_notification)

#     return render(request, 'settings/setting.html', {'notification_settings_form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import User 

@login_required
def notification_settings(request):
    user = request.user

    if request.method == 'POST':
        notifications_enabled = request.POST.get('notifications_enabled') == 'on'
        user.notifications = notifications_enabled
        user.save()
        messages.success(request, 'Notification settings updated.')
        return redirect('settings:settings')  # Redirect to user settings page
    
    return render(request, 'settings/setting.html', {'user': user})




def password_change_done(request):
    return redirect('users-settings')  # Replace with the appropriate URL name
