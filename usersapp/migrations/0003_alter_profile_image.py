# Generated by Django 5.0.3 on 2024-03-27 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersapp', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]