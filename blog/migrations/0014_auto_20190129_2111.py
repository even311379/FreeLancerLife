# Generated by Django 2.1.5 on 2019-01-29 13:11

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_landingpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpost',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('code', wagtail.core.blocks.TextBlock()), ('code_output', wagtail.core.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('wag_code', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')], help_text='Coding language', label='Language')), ('code', wagtail.core.blocks.TextBlock(label='Code'))], label='Code'))], blank=True, null=True),
        ),
    ]
