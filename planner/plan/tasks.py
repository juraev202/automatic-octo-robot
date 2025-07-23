# plan/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Plan
from .telegram_utils import send_telegram_message

@shared_task
def send_reminder(plan_id):
    try:
        plan = Plan.objects.get(id=plan_id)
        user = plan.user
        if user.telegram_id:
            message = f"⏰ Reminder for: {plan.title} at {plan.reminder_time.strftime('%Y-%m-%d %H:%M')}"
            send_telegram_message(user.telegram_id, message)
            plan.reminder_sent = True
            plan.save()
    except Plan.DoesNotExist:
        pass
