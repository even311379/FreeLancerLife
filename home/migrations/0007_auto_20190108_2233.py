# Generated by Django 2.1.4 on 2019-01-08 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20190108_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmedata',
            name='receive_time',
            field=models.DateTimeField(),
        ),
    ]
