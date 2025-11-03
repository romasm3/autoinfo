import polib
import os

os.makedirs('locale/lt/LC_MESSAGES', exist_ok=True)

po = polib.pofile('locale/lt/LC_MESSAGES/django.po')
po.save_as_mofile('locale/lt/LC_MESSAGES/django.mo')

print("✅ Compiled!")
