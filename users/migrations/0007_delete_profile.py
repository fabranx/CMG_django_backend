# Generated by Django 4.0.1 on 2022-01-20 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]