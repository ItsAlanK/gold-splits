# Generated by Django 4.0.1 on 2022-01-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_categories_category_rename_comments_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='hero_image',
            field=models.FileField(blank=True, upload_to='media/'),
        ),
    ]
