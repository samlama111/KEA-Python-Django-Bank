# Generated by Django 4.1.1 on 2022-10-02 16:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account_management_app', '0004_account_is_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledger',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='ledger',
            unique_together={('transaction_id', 'account')},
        ),
    ]