from django.db.models import TextField
from wagtail.admin.edit_handlers import FieldPanel

class MarkdownField(TextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MarkdownPanel(FieldPanel):
    def __init__(self, field_name, classname="", widget=None, **kwargs):
        super().__init__(
            field_name,
            classname=classname,
            widget=widget,
            **kwargs
            )

        if self.classname:
            if 'markdown' not in self.classname:
                self.classname += "markdown"
        else:
            self.classname = "markdown"

