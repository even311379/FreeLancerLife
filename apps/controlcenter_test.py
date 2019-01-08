from controlcenter import Dashboard, widgets
from blog.models import BlogCategory

class ModelItemList(widgets.ItemList):
    model = BlogCategory
    list_display = ('pk', 'field')

class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )