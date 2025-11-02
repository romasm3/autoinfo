# ============================================
# AUTOINFO - CONFIG PACKAGE
# ============================================
# LOKACIJA: /autoinfo/config/__init__.py
# PASKIRTIS: Python package marker
#
# Šis failas leidžia Python traktuoti 'config'
# direktoriją kaip Python package
# ============================================

# Import Celery app for auto-discovery
from .celery import app as celery_app

__all__ = ('celery_app',)
