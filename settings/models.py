# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserNotification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - Notifications: {self.notifications_enabled}'
