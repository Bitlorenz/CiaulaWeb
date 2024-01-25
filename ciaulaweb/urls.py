from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from django.conf import settings
from ciaulaweb.views import HomeView

#  from ciaulaweb.initcmds import erase_db, init_db

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('attractions/', include('attractions.urls')),
    path('HolidayPlanning/', include('HolidayPlanning.urls')),
    path('profiles/', include('profiles.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#  erase_db()
#  init_db()
