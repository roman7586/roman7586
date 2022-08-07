from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Post(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('helps', 'Хилы'),
        ('dd', 'ДД'),
        ('sales', 'Торговцы'),
        ('gildmasters', 'Гилдмастеры'),
        ('quests', 'Квестигры'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('Potions', 'Зельевары'),
        ('Wizards', 'Мастера заклинаний'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=11, choices=TYPE, default='tanks')
    text = models.TextField()
    content = models.FileField(upload_to=user_directory_path)

    #def __str__(self):
    #    return f'{self.title} by {self.user}, {self.category}.'
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Otvet(models.Model):
    Otvet_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Otvet_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    confirm = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.response_user}. {self.creation}: {self.text}'