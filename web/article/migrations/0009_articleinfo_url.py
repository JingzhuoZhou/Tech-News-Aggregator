# Generated by Django 4.2 on 2023-08-31 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_articleinfo_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleinfo',
            name='url',
            field=models.CharField(default='', max_length=100),
        ),
    ]
