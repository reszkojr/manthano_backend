# Generated by Django 4.2.6 on 2024-08-03 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_alter_message_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='professor_managed',
            field=models.BooleanField(default=False),
        ),
    ]
