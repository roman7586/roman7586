# Generated by Django 4.0.5 on 2022-07-24 18:44

import announcement.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreation', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=128)),
                ('category', models.CharField(choices=[('tanks', 'Танки'), ('helps', 'Хилы'), ('dd', 'ДД'), ('sales', 'Торговцы'), ('gildmasters', 'Гилдмастеры'), ('quests', 'Квестигры'), ('blacksmiths', 'Кузнецы'), ('tanners', 'Кожевники'), ('Potions', 'Зельевары'), ('Wizards', 'Мастера заклинаний')], default='tanks', max_length=11)),
                ('text', models.TextField()),
                ('content', models.FileField(upload_to=announcement.models.author_directory_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcement.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('dateCreation', models.DateTimeField(auto_now_add=True)),
                ('rating', models.SmallIntegerField(default=0)),
                ('commentPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcement.post')),
                ('commentUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
