from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, re_path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from blog import views as blog_views
from apps import views as apps_views
from home import views as home_views

from django.views.generic import TemplateView

from apps  import dash_test, fish_map, table_demo, map_anim_demo, map_demo

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    path('', blog_views.root),
    url(r'^search/$', search_views.search, name='search'),
    path('zh/reply_contact', home_views.reply_contact),
    path('en/reply_contact', home_views.reply_contact),
    path('add_subscribe', home_views.add_subscribe),
    path('test', blog_views.test, name='test'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    # path('zh/dash_test', TemplateView.as_view(template_name = 'dash_test.html'), name='dash_test'),
    # path('paypal_test',apps_views.pay_process, name = 'paypal_test'),
    # path('my_return_view',apps_views.my_return_view, name = 'my_return_view'),
    # path('my_cancel_view',apps_views.my_cancel_view, name = 'my_cancel_view'),
    # url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'', include(wagtail_urls)),

]




if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    from django.conf.urls.static import static
    from django.views.static import serve
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})]
