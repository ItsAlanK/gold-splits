# Generated by Django 4.0.1 on 2022-01-20 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_alter_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.FileField(blank=True, default='../static/media/placeholder-avatar.png', upload_to='media/'),
        ),
    ]
