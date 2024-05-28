# Generated by Django 3.2.25 on 2024-05-28 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rocketapi', '0004_auto_20240527_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='payee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='rocketapi.payee'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='rocketapi.payee'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('S', 'Scheduled'), ('P', 'Paid'), ('R', 'Rejected')], default='P', max_length=1),
        ),
    ]
