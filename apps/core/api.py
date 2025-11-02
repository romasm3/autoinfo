"""
╔══════════════════════════════════════════════════════════╗
║  API INTEGRATION                                         ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/api.py                   ║
║  PASKIRTIS: API integracija su visais provideriais      ║
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
        result = api.get_report(vin)

        if result['success']:
            # Konvertuoti į standartinį formatą
            return {
                'vin': vin,
                'provider': 'carfax',
                'score': result['report_data'].get('score', 0),
                'accidents': result['report_data'].get('accidents', 0),
                'owners': result['report_data'].get('owners', 0),
                'service_records': result['report_data'].get('service_records', 0),
                'title_info': result['report_data'].get('title_info', 'Unknown'),
                'raw_data': result['report_data'],
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
            'mileage_records': [
                {'date': '2023-01-15', 'odometer': 45000, 'source': 'Service'},
                {'date': '2022-06-20', 'odometer': 38000, 'source': 'Inspection'},
            ],
            'demo': True
        }


def fetch_autocheck_report(vin):
    """Autocheck API integracija"""
    api_key = settings.AUTOCHECK_API_KEY

    # DEMO MODE
    if not api_key or settings.DEBUG:
        logger.info(f"Autocheck DEMO mode for VIN: {vin}")
        return {
            'vin': vin,
            'provider': 'autocheck',
            'score': 85,
            'accidents': 1,
            'owners': 1,
            'title_info': 'Clean',
            'vehicle_use': 'Personal',
            'demo': True
        }

    # TODO: Pridėti tikrą Autocheck API integracij ą
    return None


def fetch_nmvtis_report(vin):
    """NMVTIS API integracija"""
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
            'demo': True
        }

    # TODO: Pridėti tikrą NMVTIS API integraciją
    return None
