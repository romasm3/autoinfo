"""
╔══════════════════════════════════════════════════════════╗
║  AUTOINFO - ROOT URL CONFIGURATION                       ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/config/urls.py                     ║
║  PASKIRTIS: Pagrindiniai URL routings + i18n + Rosetta  ║
╚══════════════════════════════════════════════════════════╝
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ═══════════════════════════════════════════════════════
# MAIN URL PATTERNS (WITHOUT LANGUAGE PREFIX)
# ═══════════════════════════════════════════════════════
urlpatterns = [
    # Language switcher - MUST BE FIRST!
    path('i18n/', include('django.conf.urls.i18n')),

    # Admin panel
    path('admin/', admin.site.urls),

    # Rosetta - Translation Management (admin only)
    path('rosetta/', include('rosetta.urls')),

    # Core app URLs - EVERYTHING goes through apps.core.urls
    path('', include('apps.core.urls')),
]

# ═══════════════════════════════════════════════════════
# DEVELOPMENT: SERVE STATIC & MEDIA FILES
# ═══════════════════════════════════════════════════════
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ═══════════════════════════════════════════════════════
# ADMIN CUSTOMIZATION
# ═══════════════════════════════════════════════════════
admin.site.site_header = "AutoInfo Administration"
admin.site.site_title = "AutoInfo Admin"
admin.site.index_title = "Dashboard"
