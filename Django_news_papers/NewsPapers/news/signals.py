from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post, Category


@receiver(m2m_changed, sender = Post.category.through)
def notify_subscribers(sender, instance, action = "post_add",  **kwargs):
    print(instance.category.all())
    emails = []
    for subs in instance.category.all():
        for sub in subs.subscribers.all():
            if sub.email:
                if sub.email not in emails:
                    print(sub.email, instance.id)
                    emails.append(sub.email)

    send_mail(
        subject=f'Новая статья: {instance.title}',
        message=f'{instance.text[:50]}\n Ссылка на статью: http://127.0.0.1:8000/news/{instance.id}',
        from_email= None,
        recipient_list=emails
    )