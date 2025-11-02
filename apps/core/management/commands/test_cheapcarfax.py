"""
Test CheapCarfax API command
Usage: python manage.py test_cheapcarfax
"""

from django.core.management.base import BaseCommand
from apps.core.cheapcarfax import CheapCarfaxAPI


class Command(BaseCommand):
    help = 'Test CheapCarfax API connection'

    def handle(self, *args, **options):
        self.stdout.write('Testing CheapCarfax API...\n')

        api = CheapCarfaxAPI()

        # Test 1: Check balance
        self.stdout.write('1. Checking balance...')
        balance = api.check_balance()
        if balance['success']:
            self.stdout.write(self.style.SUCCESS(
                f'   ✓ Balance: {balance["balance"]} {balance["currency"]}'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f'   ✗ Error: {balance.get("error")}'
            ))

        # Test 2: Check VIN availability
        test_vin = '1HGBH41JXMN109186'
        self.stdout.write(f'\n2. Checking VIN availability: {test_vin}')
        check = api.check_vin_availability(test_vin)
        if check['success']:
            available = check.get('available', False)
            if available:
                self.stdout.write(self.style.SUCCESS(f'   ✓ VIN available'))
            else:
                self.stdout.write(self.style.WARNING(f'   ! VIN not available'))
        else:
            self.stdout.write(self.style.ERROR(f'   ✗ Error'))

        # Test 3: Get report (optional)
        self.stdout.write(f'\n3. Testing report generation...')
        self.stdout.write(self.style.WARNING(
            '   Skipping (costs credits). Use get_report() manually.'
        ))

        self.stdout.write('\n' + self.style.SUCCESS('Tests complete!'))
