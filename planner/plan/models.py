from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom user model with Telegram chat ID
class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username

# Category model
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

# Plan model
class Plan(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    reminder_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.reminder_time.strftime('%Y-%m-%d %H:%M') if self.reminder_time else 'No time set'}"
