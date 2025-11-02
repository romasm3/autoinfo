"""
╔══════════════════════════════════════════════════════════╗
║  AUTOINFO - ROOT URL CONFIGURATION                       ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/config/urls.py                     ║
║  PASKIRTIS: Pagrindiniai URL routings                   ║
╚══════════════════════════════════════════════════════════╝
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Core app URLs - VISKAS perduodama į apps.core.urls
    path('', include('apps.core.urls')),
]

# Development: serve static ir media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin customization
admin.site.site_header = "AutoInfo Administration"
admin.site.site_title = "AutoInfo Admin"
admin.site.index_title = "Dashboard"
