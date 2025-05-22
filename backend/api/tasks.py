from celery import shared_task
import time

@shared_task(queue='notifications')
def send_notification(email, message):
    print(f"Sending notification to {email}: {message}")
    time.sleep(2)
    return f"Notification sent to {email}"