# Generated by Django 4.0.1 on 2022-01-20 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.FileField(blank=True, default='placeholder', upload_to='media/'),
        ),
    ]
