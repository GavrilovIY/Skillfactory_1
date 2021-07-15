import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail

from django.contrib.auth.models import User

from news.models import Post, Category

import datetime

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    posts = Post.objects.all().filter(time_add__gt=datetime.date.today() - datetime.timedelta(days=7))
    message_text = ''
    for post in posts:
        message_text = message_text + post.title + '\n'
        message_text = message_text + f'Ссылка на статью: http://127.0.0.1:8000/news/{post.id} \n'
    category_list = Category.objects.all().filter(id__in=Post.objects.all().filter(
        time_add__gt=datetime.date.today() - datetime.timedelta(days=7)).values('category')).values('subscribers')
    user_list = User.objects.filter(id__in=category_list)
    email_list = [i.get('email') for i in user_list.values('email')]
    send_mail(
        subject=f'За нкеделю вышли новые статьи',
        message=message_text,
        from_email=None,
        recipient_list=email_list
    )



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")