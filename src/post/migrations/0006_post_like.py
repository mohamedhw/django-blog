# Generated by Django 3.2.3 on 2021-05-28 12:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, null=True, related_name='like_button', to=settings.AUTH_USER_MODEL),
        ),
    ]
