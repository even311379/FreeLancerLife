# Generated by Django 2.1.4 on 2018-12-31 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20181231_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpage',
            name='intro',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
