"""
╔══════════════════════════════════════════════════════════╗
║  API INTEGRATION - FIXED                                 ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/api.py                   ║
║  PASKIRTIS: API integracija su visais provideriais      ║
║  ✅ FIXED: Dabar išsaugo HTML iš CheapCarfax             ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
from django.conf import settings
import logging
from .cheapcarfax import CheapCarfaxAPI

logger = logging.getLogger(__name__)


def fetch_vehicle_report(vin, report_type):
    """
    Pagrindinis entry point - gauna ataskaitą pagal tipą

    Args:
        vin (str): 17 simbolių VIN numeris
        report_type (str): 'carfax', 'autocheck' arba 'nmvtis'

    Returns:
        dict: Ataskaitos duomenys arba None
    """
    if report_type == 'carfax':
        return fetch_carfax_report(vin)
    elif report_type == 'autocheck':
        return fetch_autocheck_report(vin)
    elif report_type == 'nmvtis':
        return fetch_nmvtis_report(vin)
    else:
        logger.error(f"Unknown report type: {report_type}")
        return None


def fetch_carfax_report(vin):
    """
    Carfax API integracija per CheapCarfax

    Production: Naudoja CheapCarfax API
    Development: Grąžina demo duomenis jei nėra API key
    """
    api_key = settings.CHEAPCARFAX_API_KEY

    # PRODUCTION MODE - tikra API
    if api_key:
        logger.info(f"Fetching Carfax report for VIN: {vin}")
        api = CheapCarfaxAPI()
        result = api.get_carfax_html(vin)  # ✅ FIXED: Naudojam get_carfax_html

        if result['success']:
            # ✅ FIXED: Išsaugome HTML ir visus duomenis
            return {
                'vin': vin,
                'provider': 'carfax',
                'score': result['report_data'].get('score', 72),
                'accidents': result['report_data'].get('accidents', 0),
                'owners': result['report_data'].get('owners', 1),
                'service_records': result.get('report_data', {}).get('service_records', 0),
                'title_info': result.get('report_data', {}).get('title_info', 'Unknown'),
                'yearMakeModel': result.get('yearMakeModel', ''),  # ✅ Vehicle info
                'html': result.get('html', ''),  # ✅ SVARBIAUSIA - HTML reportas!
                'raw_data': result,  # ✅ Visi duomenys
                'demo': False
            }
        else:
            logger.error(f"CheapCarfax API error: {result.get('error')}")
            return None

    # DEMO MODE - test duomenys
    else:
        logger.info(f"Carfax DEMO mode for VIN: {vin}")
        return {
            'vin': vin,
            'provider': 'carfax',
            'score': 72,
            'accidents': 0,
            'owners': 2,
            'service_records': 15,
            'title_info': 'Clean',
            'html': '<h1>Demo Report</h1><p>This is a demo report. Enable API to see real data.</p>',
            'mileage_records': [
                {'date': '2023-01-15', 'odometer': 45000, 'source': 'Service'},
                {'date': '2022-06-20', 'odometer': 38000, 'source': 'Inspection'},
            ],
            'demo': True
        }


def fetch_autocheck_report(vin):
    """Autocheck API integracija"""
    api_key = settings.CHEAPCARFAX_API_KEY

    # PRODUCTION MODE
    if api_key:
        logger.info(f"Fetching Autocheck report for VIN: {vin}")
        api = CheapCarfaxAPI()
        result = api.get_autocheck_html(vin)  # ✅ FIXED

        if result['success']:
            # ✅ FIXED: Išsaugome HTML
            return {
                'vin': vin,
                'provider': 'autocheck',
                'score': result['report_data'].get('score', 80),
                'accidents': result['report_data'].get('accidents', 0),
                'owners': result['report_data'].get('owners', 1),
                'title_info': result.get('report_data', {}).get('title_info', 'Unknown'),
                'yearMakeModel': result.get('yearMakeModel', ''),
                'html': result.get('html', ''),  # ✅ HTML reportas
                'raw_data': result,
                'demo': False
            }
        else:
            logger.error(f"Autocheck API error: {result.get('error')}")
            return None

    # DEMO MODE
    else:
        logger.info(f"Autocheck DEMO mode for VIN: {vin}")
        return {
            'vin': vin,
            'provider': 'autocheck',
            'score': 85,
            'accidents': 1,
            'owners': 1,
            'title_info': 'Clean',
            'vehicle_use': 'Personal',
            'html': '<h1>Demo Autocheck Report</h1><p>Enable API to see real data.</p>',
            'demo': True
        }


def fetch_nmvtis_report(vin):
    """
    NMVTIS API integracija
    NOTE: CheapCarfax API neturi NMVTIS endpoint,
    tad šis naudoja demo duomenis arba kitą API
    """
    api_key = settings.NMVTIS_API_KEY

    # DEMO MODE
    if not api_key or settings.DEBUG:
        logger.info(f"NMVTIS DEMO mode for VIN: {vin}")
        return {
            'vin': vin,
            'provider': 'nmvtis',
            'score': 90,
            'accidents': 0,
            'owners': 1,
            'brand_history': 'None',
            'salvage': False,
            'junk': False,
            'html': '<h1>Demo NMVTIS Report</h1><p>Enable NMVTIS API to see real data.</p>',
            'demo': True
        }

    # TODO: Pridėti tikrą NMVTIS API integraciją
    return None
