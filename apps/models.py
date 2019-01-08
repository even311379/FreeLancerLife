from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from blog import models as blog_model

from wagtailtrans.models import TranslatablePage
# Create your models here.

class AppIndex(TranslatablePage):
    pass
