import polib
import os

LANGUAGES = ['pl', 'lt', 'lv', 'ru', 'de', 'es', 'fr']

print("=" * 60)
print("COMPILING TRANSLATIONS")
print("=" * 60)

compiled = 0

for lang in LANGUAGES:
    po_file = f'locale/{lang}/LC_MESSAGES/django.po'
    mo_file = f'locale/{lang}/LC_MESSAGES/django.mo'

    if os.path.exists(po_file):
        try:
            po = polib.pofile(po_file)
            po.save_as_mofile(mo_file)
            print(f"OK {lang.upper()}: Compiled!")
            compiled += 1
        except Exception as e:
            print(f"ERROR {lang.upper()}: {e}")
    else:
        print(f"SKIP {lang.upper()}: {po_file} not found")

print("\n" + "=" * 60)
print(f"Compiled: {compiled}")
print("=" * 60)
print("\nRun: python manage.py runserver")
