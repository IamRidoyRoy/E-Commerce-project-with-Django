# Generated by Django 3.1 on 2022-02-18 18:18

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0002_variation'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='variation',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]