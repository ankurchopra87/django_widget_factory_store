# Generated by Django 2.0.5 on 2018-05-17 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20180515_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='county',
            field=models.CharField(blank=True, max_length=50, verbose_name='County'),
        ),
        migrations.AlterField(
            model_name='address',
            name='department',
            field=models.CharField(blank=True, max_length=50, verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, max_length=50, verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='address',
            name='municipality',
            field=models.CharField(blank=True, max_length=50, verbose_name='Municipality'),
        ),
        migrations.AlterField(
            model_name='address',
            name='nation',
            field=models.CharField(blank=True, max_length=50, verbose_name='Nation'),
        ),
        migrations.AlterField(
            model_name='address',
            name='prefecture',
            field=models.CharField(blank=True, max_length=50, verbose_name='Prefecture'),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(blank=True, max_length=50, verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, max_length=50, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=50, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.CharField(blank=True, max_length=150, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveIntegerField(default=3, verbose_name='Status'),
        ),
    ]
