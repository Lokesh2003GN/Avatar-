# Generated by Django 4.2.16 on 2024-12-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_character_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='priority',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
