"""
╔══════════════════════════════════════════════════════════╗
║  CHEAPCARFAX API INTEGRATION (FIXED)                     ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/cheapcarfax.py           ║
║  PASKIRTIS: CheapCarfax API calls                       ║
║  DOCS: https://panel.cheapcarfax.net/api/docs           ║
║  ✅ FIXED: Authentication header corrected               ║
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
        self.base_url = 'https://panel.cheapcarfax.net/api'

        # ✅ FIXED: Headers pagal API dokumentaciją
        # API dokumentacija: "Every request to the API must include the x-api-key header"
        self.headers = {
            'x-api-key': self.api_key,  # ✅ CORRECT!
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_report_info(self, vin):
        """
        GET /api/reports/{VIN}
        Get the information of a report by VIN

        Returns:
            dict: {
                'success': bool,
                'vehicle': dict,
                'carfax_records': int,
                'autocheck_records': int,
                'sticker': str
            }
        """
        try:
            url = f'{self.base_url}/reports/{vin.upper()}'
            logger.info(f"Getting report info for VIN: {vin}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            logger.info(f"Report info response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Report info retrieved for VIN: {vin}")
                return {
                    'success': True,
                    'vehicle': data.get('vehicle', {}),
                    'carfax_records': data.get('carfax_records', 0),
                    'autocheck_records': data.get('autocheck_records', 0),
                    'sticker': data.get('sticker', 'false')
                }
            elif response.status_code == 401:
                logger.error("Unauthorized - check API key")
                return {'success': False, 'error': 'Invalid API key'}
            else:
                logger.error(f"Report info failed: {response.status_code} - {response.text}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}

        except Exception as e:
            logger.error(f"Report info exception: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_user_info(self):
        """
        GET /api/user
        Get the user information

        Returns:
            dict: {
                'success': bool,
                '_id': str,
                'email': str,
                'role': str
            }
        """
        try:
            url = f'{self.base_url}/user'
            logger.info(f"Getting user info")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            logger.info(f"User info response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"User info retrieved")
                return {
                    'success': True,
                    '_id': data.get('_id'),
                    'email': data.get('email'),
                    'role': data.get('role')
                }
            elif response.status_code == 401:
                logger.error("Unauthorized - check API key")
                return {'success': False, 'error': 'Invalid API key'}
            else:
                logger.error(f"User info failed: {response.status_code} - {response.text}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}

        except Exception as e:
            logger.error(f"User info exception: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_user_limits(self):
        """
        GET /api/user/limits
        Get the user's current limit information

        Returns:
            dict: {
                'success': bool,
                'daily_limit': int,
                'carfax_reports_left_today': int,
                'autocheck_reports_left_today': int,
                'credits': int
            }
        """
        try:
            url = f'{self.base_url}/user/limits'
            logger.info(f"Getting user limits")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            logger.info(f"User limits response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"User limits: {data.get('credits', 0)} credits remaining")
                return {
                    'success': True,
                    'daily_limit': data.get('daily_limit', 0),
                    'carfax_reports_left_today': data.get('carfax_reports_left_today', 0),
                    'autocheck_reports_left_today': data.get('autocheck_reports_left_today', 0),
                    'credits': data.get('credits', 0)
                }
            elif response.status_code == 401:
                logger.error("Unauthorized - check API key")
                return {'success': False, 'error': 'Invalid API key'}
            else:
                logger.error(f"User limits failed: {response.status_code} - {response.text}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}

        except Exception as e:
            logger.error(f"User limits exception: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_carfax_html(self, vin):
        """
        GET /api/carfax/vin/:vin/html
        Get the Carfax report as HTML for a VIN

        NOTE: You can use 'JH4DC4360SS001610' as a test VIN to not use up your credits.

        Args:
            vin (str): 17 character VIN number

        Returns:
            dict: {
                'success': bool,
                'yearMakeModel': str,
                'id': str,
                'html': str
            }
        """
        try:
            url = f'{self.base_url}/carfax/vin/{vin.upper()}/html'
            logger.info(f"Getting Carfax HTML for VIN: {vin}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=30
            )

            logger.info(f"Carfax HTML response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Carfax HTML generated for VIN: {vin}")

                # Parse the report data
                parsed_data = self._parse_carfax_data(data)

                return {
                    'success': True,
                    'vin': vin,
                    'yearMakeModel': data.get('yearMakeModel', ''),
                    'id': data.get('id', ''),
                    'html': data.get('html', ''),
                    'report_data': parsed_data,
                    'provider': 'carfax',
                    'raw_data': data
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
                logger.error(f"Carfax HTML failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'API Error: {response.status_code}'
                }

        except requests.exceptions.Timeout:
            logger.error(f"Timeout for VIN: {vin}")
            return {'success': False, 'error': 'Request timeout'}
        except Exception as e:
            logger.error(f"Carfax HTML exception for VIN {vin}: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_autocheck_html(self, vin):
        """
        GET /api/autocheck/vin/:vin/html
        Get the Autocheck report as HTML for a VIN

        NOTE: You can use 'JH4DC4360SS001610' as a test VIN to not use up your credits.

        Args:
            vin (str): 17 character VIN number

        Returns:
            dict: {
                'success': bool,
                'yearMakeModel': str,
                'id': str,
                'html': str
            }
        """
        try:
            url = f'{self.base_url}/autocheck/vin/{vin.upper()}/html'
            logger.info(f"Getting Autocheck HTML for VIN: {vin}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=30
            )

            logger.info(f"Autocheck HTML response: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Autocheck HTML generated for VIN: {vin}")

                # Parse the report data
                parsed_data = self._parse_autocheck_data(data)

                return {
                    'success': True,
                    'vin': vin,
                    'yearMakeModel': data.get('yearMakeModel', ''),
                    'id': data.get('id', ''),
                    'html': data.get('html', ''),
                    'report_data': parsed_data,
                    'provider': 'autocheck',
                    'raw_data': data
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
                logger.error(f"Autocheck HTML failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'API Error: {response.status_code}'
                }

        except requests.exceptions.Timeout:
            logger.error(f"Timeout for VIN: {vin}")
            return {'success': False, 'error': 'Request timeout'}
        except Exception as e:
            logger.error(f"Autocheck HTML exception for VIN {vin}: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_report(self, vin, report_type='carfax'):
        """
        Get report based on type (carfax or autocheck)

        Args:
            vin (str): 17 character VIN number
            report_type (str): 'carfax' or 'autocheck'

        Returns:
            dict: Report data
        """
        if report_type == 'carfax':
            return self.get_carfax_html(vin)
        elif report_type == 'autocheck':
            return self.get_autocheck_html(vin)
        else:
            return {
                'success': False,
                'error': f'Unknown report type: {report_type}'
            }

    def _parse_carfax_data(self, data):
        """
        Parse Carfax HTML data into standardized format

        Args:
            data (dict): Raw API response

        Returns:
            dict: Standardized report data
        """
        # Extract key metrics from HTML if possible
        # For now, return basic structure
        parsed = {
            'score': 75,  # Default score
            'accidents': 0,
            'owners': 1,
            'service_records': 0,
            'title_info': 'Unknown',
            'vehicle_info': {
                'yearMakeModel': data.get('yearMakeModel', ''),
                'id': data.get('id', ''),
            }
        }

        return parsed

    def _parse_autocheck_data(self, data):
        """
        Parse Autocheck HTML data into standardized format

        Args:
            data (dict): Raw API response

        Returns:
            dict: Standardized report data
        """
        # Extract key metrics from HTML if possible
        # For now, return basic structure
        parsed = {
            'score': 80,  # Default score
            'accidents': 0,
            'owners': 1,
            'title_info': 'Unknown',
            'vehicle_info': {
                'yearMakeModel': data.get('yearMakeModel', ''),
                'id': data.get('id', ''),
            }
        }

        return parsed


# Helper functions for easy use
def get_carfax_report(vin):
    """
    Simplified function to get Carfax report

    Usage:
        result = get_carfax_report('1HGBH41JXMN109186')
        if result['success']:
            print(result['html'])

    Args:
        vin (str): 17 character VIN number

    Returns:
        dict: Report result
    """
    api = CheapCarfaxAPI()
    return api.get_carfax_html(vin)


def get_autocheck_report(vin):
    """
    Simplified function to get Autocheck report

    Usage:
        result = get_autocheck_report('1HGBH41JXMN109186')
        if result['success']:
            print(result['html'])

    Args:
        vin (str): 17 character VIN number

    Returns:
        dict: Report result
    """
    api = CheapCarfaxAPI()
    return api.get_autocheck_html(vin)


def check_api_limits():
    """
    Check current API limits and credits

    Usage:
        limits = check_api_limits()
        print(f"Credits remaining: {limits['credits']}")

    Returns:
        dict: Limits information
    """
    api = CheapCarfaxAPI()
    return api.get_user_limits()
