# Generated by Django 4.0.4 on 2022-04-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorder',
            old_name='amount',
            new_name='_amount',
        ),
        migrations.AlterField(
            model_name='productorder',
            name='_amount',
            field=models.IntegerField(db_column='amount', default=1),
        ),
    ]