# Generated by Django 4.0.1 on 2022-01-13 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='prof_img'),
        ),
    ]