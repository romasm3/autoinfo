"""
╔══════════════════════════════════════════════════════════╗
║  CHEAPCARFAX API INTEGRATION                             ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/cheapcarfax.py           ║
║  PASKIRTIS: CheapCarfax API calls                       ║
║  DOCS: https://panel.cheapcarfax.net/api/docs           ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class CheapCarfaxAPI:
    """CheapCarfax API Client"""

    def __init__(self):
        self.api_key = settings.CHEAPCARFAX_API_KEY
        self.base_url = settings.CHEAPCARFAX_API_URL.rstrip('/')

        # Headers pagal dokumentaciją
        self.headers = {
            'api-key': self.api_key,  # ← PAKEISTA! Ne Bearer, o api-key
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def check_balance(self):
        """
        GET /balance
        Patikrinti API sąskaitos balansą
        """
        try:
            url = f'{self.base_url}/balance'
            logger.info(f"Checking balance: {url}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            logger.info(f"Balance response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"CheapCarfax balance: {data.get('balance', 0)} credits")
                return {
                    'success': True,
                    'balance': data.get('balance', 0),
                    'currency': data.get('currency', 'credits')
                }
            elif response.status_code == 401:
                logger.error("Unauthorized - check API key")
                return {'success': False, 'error': 'Invalid API key'}
            else:
                logger.error(f"Balance check failed: {response.status_code} - {response.text}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}

        except Exception as e:
            logger.error(f"Balance check exception: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_report(self, vin):
        """
        POST /report
        Gauti Carfax reportą pagal VIN

        Args:
            vin (str): 17 simbolių VIN numeris

        Returns:
            dict: Report data arba error
        """
        try:
            url = f'{self.base_url}/report'
            payload = {'vin': vin.upper()}

            logger.info(f"Getting report for VIN: {vin}")

            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=30
            )

            logger.info(f"Report response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Report generated for VIN: {vin}")
                return {
                    'success': True,
                    'vin': vin,
                    'report_data': data,
                    'provider': 'cheapcarfax'
                }
            elif response.status_code == 404:
                logger.warning(f"VIN not found: {vin}")
                return {
                    'success': False,
                    'error': 'VIN not found in database'
                }
            elif response.status_code == 402:
                logger.error("Insufficient credits")
                return {
                    'success': False,
                    'error': 'Insufficient API credits'
                }
            elif response.status_code == 401:
                logger.error("Unauthorized")
                return {
                    'success': False,
                    'error': 'Invalid API key'
                }
            else:
                logger.error(f"Report failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'API Error: {response.status_code}'
                }

        except requests.exceptions.Timeout:
            logger.error(f"Timeout for VIN: {vin}")
            return {'success': False, 'error': 'Request timeout'}
        except Exception as e:
            logger.error(f"Report exception for VIN {vin}: {str(e)}")
            return {'success': False, 'error': str(e)}

    def check_vin_availability(self, vin):
        """
        GET /check/{vin}
        Patikrinti ar VIN yra duomenų bazėje (nemokamai)
        """
        try:
            url = f'{self.base_url}/check/{vin.upper()}'
            logger.info(f"Checking VIN availability: {url}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            logger.info(f"Check VIN response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'available': data.get('available', False),
                    'vin': vin
                }
            elif response.status_code == 401:
                return {'success': False, 'error': 'Invalid API key'}
            else:
                logger.error(f"Check failed: {response.text}")
                return {'success': False, 'available': False, 'error': response.text}

        except Exception as e:
            logger.error(f"Check VIN exception: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_report_history(self, limit=10):
        """
        GET /reports
        Gauti reportų istoriją
        """
        try:
            url = f'{self.base_url}/reports'
            params = {'limit': limit}

            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'reports': data.get('reports', []),
                    'total': data.get('total', 0)
                }
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}

        except Exception as e:
            logger.error(f"History exception: {str(e)}")
            return {'success': False, 'error': str(e)}


# Helper function
def get_cheapcarfax_report(vin):
    """
    Supaprastinta funkcija reportui gauti

    Usage:
        result = get_cheapcarfax_report('1HGBH41JXMN109186')
        if result['success']:
            print(result['report_data'])
    """
    api = CheapCarfaxAPI()
    return api.get_report(vin)
