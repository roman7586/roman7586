from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def user_directory_path(instance, filename): # Создание папки с контентом под каждого пользователя
    return 'user_{0}/{1}'.format(instance.user.id, filename)
    
class ChatUser(User):
    avatar = models.ImageField(upload_to=user_directory_path, default='avatars/default.jpg')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(150, 150)],
                                      format='JPEG',
                                      options={'quality': 100})

class Room(models.Model):
    name = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from='name', unique=True)
    user = models.ForeignKey(ChatUser, related_name='room_user', on_delete=models.CASCADE, db_constraint=False, null=True)
    private = models.BooleanField(default=False)
 
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages_room', on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser, related_name='messages_user', on_delete=models.CASCADE, db_constraint=False)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('date_added',)