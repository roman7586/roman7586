from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Category


@receiver(m2m_changed, sender=Post.postCategory.through)
def notify(sender, instance, action, **kwargs):
    mass =[]
    if action == "post_add":
        for i in instance.postCategory.all():
            for j in i.subscribers.all():
                mass.append(j)                                                          #mass.append(j.email) если через получателей в копии

        for user in set(mass):                                                          #убирается, если через получателей в копии
            #send_mail(subject=f'Вышел новый пост с заголовком {instance.title} ',
            #       message=instance.text,
            #       from_email='hiromant86@yandex.ru',
            #       #здесь указываете почту, с которой будете отправлять
            #       recipient_list=[user.email]                                          #recipient_list=set(mass) , если через получателей в копии
            #          )

            #письмо в формате html
            #subject, from_email, to = 'hello', 'hiromant86@yandex.ru', [user.email]
            #text_content = 'This is an important message.'
            #html_content = '<p>This is an <strong>important</strong> message.</p>'
            html_content = render_to_string(
                'news_created.html',
                {
                    'Post': instance,
                    'Category':Category,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Вышел новый пост с заголовком {instance.title}',
                #body=instance.text,
                from_email='hiromant86@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()