# Generated by Django 4.1 on 2022-09-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_moviereview_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviereview',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
