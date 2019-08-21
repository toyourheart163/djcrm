# Generated by Django 2.2.3 on 2019-08-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_enrollment_contract_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '已报名'), (1, '未报名'), (2, '已退学')], default=1),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='Pay_cost',
            field=models.BooleanField(default=False, verbose_name='缴费'),
        ),
    ]