from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import ContactMeData

class ContactMeDataAdmin(ModelAdmin):
    model = ContactMeData
    menu_label = 'Data'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    list_display = ('name', 'organization','task','plan','due_date','email','receive_time')
    list_filter = ('plan', 'task')
    search_fields = ('receive_time')

modeladmin_register(ContactMeDataAdmin)