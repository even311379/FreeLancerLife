# Generated by Django 2.1.5 on 2019-01-29 13:39

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190129_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpost',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('wag_code', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.ChoiceBlock(choices=[('python', 'Python'), ('bash', 'Bash'), ('brainfuck', 'Brainfuck'), ('csharp', 'C#'), ('cpp', 'C++'), ('css', 'CSS'), ('django', 'Django/Jinja2'), ('http', 'HTTP'), ('java', 'Java'), ('javascript', 'JavaScript'), ('json', 'JSON')], help_text='Coding language', label='Language')), ('code', wagtail.core.blocks.TextBlock(label='Code'))], label='Code')), ('code_output', wagtail.core.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image'))], blank=True, null=True),
        ),
    ]
