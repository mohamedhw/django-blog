# Generated by Django 3.2.3 on 2021-05-28 13:14

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=1, upload_to=post.models.image_upload),
            preserve_default=False,
        ),
    ]
