# Generated by Django 5.2.4 on 2025-07-15 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.URLField(),
        ),
    ]
