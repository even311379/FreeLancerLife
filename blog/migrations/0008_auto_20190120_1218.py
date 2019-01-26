# Generated by Django 2.1.5 on 2019-01-20 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20190120_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='related_page1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailtrans.TranslatablePage'),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='related_page2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailtrans.TranslatablePage'),
        ),
        migrations.AlterField(
            model_name='postpage',
            name='related_page1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailtrans.TranslatablePage'),
        ),
        migrations.AlterField(
            model_name='postpage',
            name='related_page2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailtrans.TranslatablePage'),
        ),
    ]