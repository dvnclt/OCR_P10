# Generated by Django 5.1.3 on 2024-11-27 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_remove_user_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
    ]
