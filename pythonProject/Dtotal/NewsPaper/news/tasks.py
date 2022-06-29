import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category

@shared_task
def weekly_mailing_list():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.now().isocalendar()[1] - 1

        for news in Post.objects.filter(category_id=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'category_id__name'):
            date_format = news.get("dateCreation").strftime("%m/%d/%Y")

            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Категория: {news.get("category_id__name")}, Дата создания: {date_format}')

            news_from_each_category.append(new)

        subscribers = category.subscribers.all()

        for subscriber in subscribers:
            html_content = render_to_string(
                'sender.html', {'user': subscriber,
                                'text': news_from_each_category,
                                'category_name': category.name,
                                'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='hiromant86@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()