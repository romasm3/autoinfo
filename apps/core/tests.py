"""
UNIT TESTS
Testai modeliams, views, formoms
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Report
from decimal import Decimal


class UserProfileTestCase(TestCase):
    """UserProfile modelio testai"""

    def setUp(self):
        """Sukurti test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_created(self):
        """Testuoti ar profile automatiškai sukuriamas"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.balance, Decimal('0.00'))

    def test_add_balance(self):
        """Testuoti add_balance metodą"""
        self.user.profile.add_balance(100)
        self.assertEqual(self.user.profile.balance, Decimal('100.00'))

    def test_deduct_balance(self):
        """Testuoti deduct_balance metodą"""
        self.user.profile.add_balance(100)
        result = self.user.profile.deduct_balance(50)
        self.assertTrue(result)
        self.assertEqual(self.user.profile.balance, Decimal('50.00'))

    def test_insufficient_balance(self):
        """Testuoti insufficient balance"""
        result = self.user.profile.deduct_balance(100)
        self.assertFalse(result)


class ReportTestCase(TestCase):
    """Report modelio testai"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_report(self):
        """Testuoti report sukūrimą"""
        report = Report.objects.create(
            user=self.user,
            vin='1HGBH41JXMN109186',
            report_type='carfax',
            price_paid=Decimal('14.99'),
            score=85
        )
        self.assertEqual(report.vin, '1HGBH41JXMN109186')
        self.assertEqual(report.score, 85)
