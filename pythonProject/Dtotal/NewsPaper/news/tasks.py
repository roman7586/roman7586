import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory


@shared_task
def weekly_mailing_list():
    for post in Post.objects.filter(created__gt=(datetime.date.today() - datetime.timedelta(days=7))):
        for cat in PostCategory.objects.filter(post=post):
            for subscribe in Subscribe.objects.filter(category=cat.category):

                html_content = render_to_string(
                    'news_created.html',
                    {
                        'Post': post,
                        'Category': Category,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'Вышел новый пост с заголовком {post.title}',
                    # body=instance.text,
                    from_email='hiromant86@yandex.ru',
                    to=[subscribe.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

