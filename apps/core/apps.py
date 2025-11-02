"""
╔══════════════════════════════════════════════════════════╗
║  CORE APP CONFIGURATION                                  ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/apps.py                  ║
║  PASKIRTIS: App config (registruojamas settings.py)     ║
╚══════════════════════════════════════════════════════════╝
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'AutoInfo Core'

    def ready(self):
        # Import signals
        import apps.core.signals
