# Generated by Django 4.0.1 on 2022-01-24 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customuser_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='reviews',
        ),
    ]
