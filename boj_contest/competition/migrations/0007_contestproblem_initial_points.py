# Generated by Django 5.1 on 2024-08-25 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_rename_user_id_participant_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestproblem',
            name='initial_points',
            field=models.IntegerField(default=1000),
        ),
    ]
