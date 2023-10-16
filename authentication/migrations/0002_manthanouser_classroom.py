# Generated by Django 4.2.6 on 2023-10-16 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_alter_classroom_code_alter_classroom_description_and_more'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manthanouser',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='classroom.classroom'),
        ),
    ]
