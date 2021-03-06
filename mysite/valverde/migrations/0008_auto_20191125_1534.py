# Generated by Django 2.2.5 on 2019-11-25 14:34

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('valverde', '0007_auto_20191125_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='comments_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 25, 14, 34, 47, 72478, tzinfo=utc)),
        ),
    ]
