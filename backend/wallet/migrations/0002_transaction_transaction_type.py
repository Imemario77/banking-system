# Generated by Django 5.1.2 on 2024-10-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.SmallIntegerField(choices=[(1, 'Deposit'), (2, 'ReFund'), (3, 'Withdraw')], default=1),
        ),
    ]
