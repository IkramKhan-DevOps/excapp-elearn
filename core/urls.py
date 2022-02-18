# import notifications.urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [

    # WEBSITE APPLICATION --------------------------------------------------------------------------------
    path('', include('src.website.urls', namespace='website')),

    # ADMIN/ROOT APPLICATION
    path('admin/', admin.site.urls),
    path('accounts/', include('src.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # PORTALS ---------------------------------------------------------- #
    path('a/', include('src.portals.admins.urls', namespace='admins')),
    path('c/', include('src.portals.instructor.urls', namespace='instructor')),

]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
