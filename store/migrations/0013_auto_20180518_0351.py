# Generated by Django 2.0.5 on 2018-05-18 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20180518_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='Email Address'),
        ),
    ]
