# Generated by Django 4.0.1 on 2022-01-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_hero_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='hero_image',
            field=models.FileField(blank=True, default='placeholder', upload_to='media/'),
        ),
    ]