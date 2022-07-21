from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.authorUser.username.title()

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

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
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=2, choices=TYPE, default='tanks')
    text = models.TextField()

    #postCategory = models.ManyToManyField(Category, through='PostCategory')
    #rating = models.SmallIntegerField(default=0)