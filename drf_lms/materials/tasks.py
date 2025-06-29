from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_email(email, course_title):
    send_mail(
        subject='Обновление курса',
        message=f'Курс "{course_title}" был обновлён! Проверьте новые материалы.',
        from_email='clickandgo1346@yandex.ru',
        recipient_list=[email],
        fail_silently=False,
    )