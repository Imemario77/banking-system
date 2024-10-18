# Generated by Django 5.1.2 on 2024-10-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.SmallIntegerField(choices=[(1, 'Deposit'), (2, 'ReFund'), (3, 'Withdraw')], default=1),
        ),
    ]
