# Generated by Django 4.0.5 on 2022-07-13 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
