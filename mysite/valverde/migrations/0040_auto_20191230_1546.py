# Generated by Django 2.2.5 on 2019-12-30 14:46

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('valverde', '0039_auto_20191228_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='comments_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic_nr',
            field=models.IntegerField(blank=True, default=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 30, 14, 46, 30, 841386, tzinfo=utc)),
        ),
    ]