from django.contrib.auth.models import User
from django.db import models

# Create your models here.

def author_directory_path(instance, filename):
    return 'author_{0}/{1}'.format(instance.author.id, filename)

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
    category = models.CharField(max_length=11, choices=TYPE, default='tanks')
    text = models.TextField()
    content=models.FileField(upload_to=author_directory_path)

    #postCategory = models.ManyToManyField(Category, through='PostCategory')
    #rating = models.SmallIntegerField(default=0)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)