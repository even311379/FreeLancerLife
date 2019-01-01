# Generated by Django 2.1.4 on 2018-12-29 02:44

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='about_caption',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_context',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='data_title',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='game_title',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='title_caption',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='web_title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]