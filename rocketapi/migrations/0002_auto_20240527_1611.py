# Generated by Django 3.2.25 on 2024-05-27 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rocketapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
