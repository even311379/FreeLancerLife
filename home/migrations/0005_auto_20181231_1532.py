# Generated by Django 2.1.4 on 2018-12-31 07:32

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20181229_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='tutorial_content',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='tutorial_title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]