# user_settings/forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserNotification

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = UserNotification
        fields = ['notifications_enabled']
