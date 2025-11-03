"""
╔══════════════════════════════════════════════════════════╗
║  CHEAPCARFAX API TEST COMMAND                            ║
╠══════════════════════════════════════════════════════════╣
║  Usage: python manage.py test_cheapcarfax               ║
║  Tests: Balance, VIN check, Report generation           ║
╚══════════════════════════════════════════════════════════╝
"""

from django.core.management.base import BaseCommand
from apps.core.cheapcarfax import CheapCarfaxAPI
import json


class Command(BaseCommand):
    help = 'Test CheapCarfax API connection and functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--vin',
            type=str,
            help='Test VIN number (default: 1HGBH41JXMN109186)',
            default='1HGBH41JXMN109186'
        )
        parser.add_argument(
            '--get-report',
            action='store_true',
            help='Actually fetch a report (costs credits!)',
        )

    def handle(self, *args, **options):
        test_vin = options['vin']
        get_report = options['get_report']

        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('🚗 CheapCarfax API Test Suite'))
        self.stdout.write('=' * 60)

        api = CheapCarfaxAPI()

        # Test 1: Check Balance
        self.stdout.write('\n📊 TEST 1: Checking Account Balance')
        self.stdout.write('-' * 60)

        balance = api.check_balance()
        if balance['success']:
            self.stdout.write(self.style.SUCCESS(
                f'✅ Balance: {balance["balance"]} {balance.get("currency", "credits")}'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f'❌ Error: {balance.get("error")}'
            ))
            return

        # Test 2: Check VIN Availability
        self.stdout.write(f'\n🔍 TEST 2: Checking VIN Availability: {test_vin}')
        self.stdout.write('-' * 60)

        check = api.check_vin_availability(test_vin)
        if check['success']:
            if check.get('available'):
                self.stdout.write(self.style.SUCCESS(
                    f'✅ VIN {test_vin} is AVAILABLE in database'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'⚠️  VIN {test_vin} is NOT available in database'
                ))
        else:
            self.stdout.write(self.style.ERROR(
                f'❌ Error checking VIN: {check.get("error")}'
            ))

        # Test 3: Get Report (optional)
        if get_report:
            self.stdout.write(f'\n📄 TEST 3: Generating Report for VIN: {test_vin}')
            self.stdout.write(self.style.WARNING('⚠️  This will deduct credits from your account!'))
            self.stdout.write('-' * 60)

            report = api.get_report(test_vin)
            if report['success']:
                self.stdout.write(self.style.SUCCESS('✅ Report generated successfully!'))
                self.stdout.write('\n' + '=' * 60)
                self.stdout.write('📊 REPORT SUMMARY:')
                self.stdout.write('=' * 60)

                data = report['report_data']
                self.stdout.write(f"VIN: {report['vin']}")
                self.stdout.write(f"Score: {data.get('score', 'N/A')}/100")
                self.stdout.write(f"Accidents: {data.get('accidents', 0)}")
                self.stdout.write(f"Owners: {data.get('owners', 0)}")
                self.stdout.write(f"Service Records: {data.get('service_records', 0)}")
                self.stdout.write(f"Title: {data.get('title_info', 'Unknown')}")

                vehicle = data.get('vehicle_info', {})
                if vehicle:
                    self.stdout.write(f"\nVehicle: {vehicle.get('year')} {vehicle.get('make')} {vehicle.get('model')}")

                # Show raw data (first 500 chars)
                self.stdout.write('\n' + '-' * 60)
                self.stdout.write('📝 Raw Data (truncated):')
                self.stdout.write('-' * 60)
                raw = json.dumps(report.get('raw_data', {}), indent=2)
                self.stdout.write(raw[:500] + '...' if len(raw) > 500 else raw)
            else:
                self.stdout.write(self.style.ERROR(
                    f'❌ Error generating report: {report.get("error")}'
                ))
        else:
            self.stdout.write(f'\n📄 TEST 3: Report Generation (SKIPPED)')
            self.stdout.write('-' * 60)
            self.stdout.write('ℹ️  Use --get-report flag to actually generate a report')
            self.stdout.write(self.style.WARNING('⚠️  Note: This will cost credits!'))

        # Test 4: Report History
        self.stdout.write(f'\n📚 TEST 4: Fetching Report History (last 5)')
        self.stdout.write('-' * 60)

        history = api.get_report_history(limit=5)
        if history['success']:
            reports = history.get('reports', [])
            total = history.get('total', 0)

            self.stdout.write(self.style.SUCCESS(
                f'✅ Found {len(reports)} recent reports (Total: {total})'
            ))

            if reports:
                for i, r in enumerate(reports, 1):
                    self.stdout.write(f"\n{i}. VIN: {r.get('vin', 'Unknown')}")
                    self.stdout.write(f"   Date: {r.get('created_at', 'Unknown')}")
            else:
                self.stdout.write('   No reports found')
        else:
            self.stdout.write(self.style.ERROR(
                f'❌ Error fetching history: {history.get("error")}'
            ))

        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ All tests complete!'))
        self.stdout.write('=' * 60)

        if not get_report:
            self.stdout.write('\n💡 Tip: Run with --get-report flag to test actual report generation')
            self.stdout.write(f'   Example: python manage.py test_cheapcarfax --get-report --vin {test_vin}')
