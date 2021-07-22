from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('apps.core.urls', 'core'), namespace='core')),
]
