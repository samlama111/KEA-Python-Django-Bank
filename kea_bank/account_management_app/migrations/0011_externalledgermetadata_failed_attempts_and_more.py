# Generated by Django 4.1.1 on 2023-01-15 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_management_app', '0010_merge_20221225_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalledgermetadata',
            name='failed_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='externalledgermetadata',
            name='successful_attempts',
            field=models.IntegerField(default=0),
        ),
    ]
