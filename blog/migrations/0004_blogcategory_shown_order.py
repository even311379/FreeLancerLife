# Generated by Django 2.1.4 on 2019-01-03 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcategory_name_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='shown_order',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]