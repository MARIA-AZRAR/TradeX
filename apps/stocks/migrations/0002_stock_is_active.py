# Generated by Django 4.2.13 on 2024-09-12 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
