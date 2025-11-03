"""
Test CheapCarfax API command
Usage: python manage.py test_cheapcarfax_api
"""

from django.core.management.base import BaseCommand
from apps.core.cheapcarfax import CheapCarfaxAPI


class Command(BaseCommand):
    help = 'Test CheapCarfax API connection with all endpoints'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('TESTING CHEAPCARFAX API')
        self.stdout.write('=' * 60)

        api = CheapCarfaxAPI()

        # Test 1: User Info
        self.stdout.write('\n1. Testing GET /api/user...')
        user = api.get_user_info()
        if user['success']:
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ User: {user.get('email')} (Role: {user.get('role')})"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"   ✗ Error: {user.get('error')}"
            ))

        # Test 2: User Limits
        self.stdout.write('\n2. Testing GET /api/user/limits...')
        limits = api.get_user_limits()
        if limits['success']:
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Credits: {limits['credits']}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Daily Limit: {limits['daily_limit']}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Carfax reports left today: {limits['carfax_reports_left_today']}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Autocheck reports left today: {limits['autocheck_reports_left_today']}"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"   ✗ Error: {limits.get('error')}"
            ))

        # Test 3: Report Info (free test)
        test_vin = 'JH4DC4360SS001610'
        self.stdout.write(f'\n3. Testing GET /api/reports/{test_vin}...')
        info = api.get_report_info(test_vin)
        if info['success']:
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Vehicle: {info['vehicle'].get('year')} {info['vehicle'].get('make')} {info['vehicle'].get('model')}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Carfax records: {info['carfax_records']}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"   ✓ Autocheck records: {info['autocheck_records']}"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"   ✗ Error: {info.get('error')}"
            ))

        # Test 4: Carfax HTML (uses credits - optional)
        self.stdout.write(f'\n4. Testing GET /api/carfax/vin/{test_vin}/html...')
        self.stdout.write(self.style.WARNING(
            '   ! Skipping (uses credits). Uncomment code to test.'
        ))

        # Uncomment to test (USES CREDITS!):
        # carfax = api.get_carfax_html(test_vin)
        # if carfax['success']:
        #     self.stdout.write(self.style.SUCCESS(
        #         f"   ✓ Report generated: {carfax['yearMakeModel']}"
        #     ))
        #     self.stdout.write(self.style.SUCCESS(
        #         f"   ✓ HTML length: {len(carfax['html'])} chars"
        #     ))
        # else:
        #     self.stdout.write(self.style.ERROR(
        #         f"   ✗ Error: {carfax.get('error')}"
        #     ))

        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ API TESTS COMPLETE!'))
        self.stdout.write('=' * 60)
