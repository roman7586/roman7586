from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Otvet


@receiver(post_save, sender=Otvet)
def send_response_email(created, instance, *args, **kwargs):
    if created:
        post_author = instance.Otvet_to.user
        subject = f'{post_author}'
        otklick_user = instance.Otvet_user
        post_author_email = instance.Otvet_to.user.email

        send_mail(
            subject=subject,
            message=f"Добрый день, {post_author}\n"
                    f"Появился новый отклик на ваше обьявление от пользователя {otklick_user}",
            from_email='',
            recipient_list=[post_author_email])