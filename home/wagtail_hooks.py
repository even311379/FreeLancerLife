from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from .models import ContactMeData, SubscriberEmail

class ContactMeDataAdmin(ModelAdmin):
    model = ContactMeData
    menu_label = 'ContactMeData'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    list_display = ('name', 'organization','task','plan','due_date','email','receive_time')
    list_filter = ('plan', 'task')
    search_fields = ('name', 'organization',)

class SubscriberEmailAdmin(ModelAdmin):
    model = SubscriberEmail
    menu_label = 'SubscriberEmail'  # ditch this to use verbose_name_plural from model
    menu_icon = 'mail'  # change as required
    list_display = ('subsciber_email', 'receive_time')

class LibraryGroup(ModelAdminGroup):
    menu_label = 'Data'
    menu_icon = 'folder-open-inverse'  # change as required
    items = (ContactMeDataAdmin, SubscriberEmailAdmin)

modeladmin_register(LibraryGroup)