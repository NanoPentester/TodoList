# Generated by Django 4.2.11 on 2025-01-07 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_category_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
