# Generated by Django 2.2.3 on 2019-08-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='contract_review',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='合同审核'),
        ),
    ]