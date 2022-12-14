# Generated by Django 4.1.1 on 2022-12-20 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account_management_app', '0003_account_is_saving_account_ledger_is_saving_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('conversation_id', models.AutoField(primary_key=True, serialize=False)),
                ('json_array', models.JSONField(blank=True, default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
