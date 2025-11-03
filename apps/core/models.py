"""
DATABASE MODELIAI - PostgreSQL
Čia aprašomi visi duomenų bazės modeliai
✅ UPDATED: Pridėtas report_html field Carfax/Autocheck HTML saugojimui
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class UserProfile(models.Model):
    """
    Vartotojo profilis - praplečia Django User modelį
    Saugo balansą ir papildomą informaciją
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} - {self.balance} PLN"

    def add_balance(self, amount):
        """Pridėti pinigų į sąskaitą"""
        self.balance += Decimal(str(amount))
        self.save()
        return self.balance

    def deduct_balance(self, amount):
        """Nuskaičiuoti pinigus iš sąskaitos"""
        amount_decimal = Decimal(str(amount))
        if self.balance >= amount_decimal:
            self.balance -= amount_decimal
            self.save()
            return True
        return False

    def has_sufficient_balance(self, amount):
        """Patikrinti ar yra pakankamai pinigų"""
        return self.balance >= Decimal(str(amount))


class Report(models.Model):
    """
    VIN ataskaitos modelis
    Saugo visas sugeneruotas VIN ataskaitas
    ✅ UPDATED: Pridėtas report_html field pilnam HTML iš CheapCarfax
    """
    REPORT_TYPES = (
        ('carfax', 'Carfax'),
        ('autocheck', 'Autocheck'),
        ('nmvtis', 'NMVTIS'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    vin = models.CharField(max_length=17, db_index=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)

    # ✅ NAUJAS FIELD - Pilnas HTML reportas iš CheapCarfax API
    report_html = models.TextField(
        blank=True,
        null=True,
        help_text='Full HTML report from CheapCarfax API'
    )

    # JSON duomenys (backup)
    report_data = models.JSONField(default=dict, blank=True)

    price_paid = models.DecimalField(max_digits=10, decimal_places=2)

    # Ataskaitos rezultatai (quick access)
    score = models.IntegerField(null=True, blank=True)
    accidents = models.IntegerField(default=0)
    owners = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reports'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vin']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['report_type']),
        ]

    def __str__(self):
        return f"{self.vin} - {self.get_report_type_display()}"

    @property
    def score_color(self):
        """Grąžina spalvą pagal score"""
        if self.score is None:
            return 'gray'
        if self.score >= 70:
            return 'green'
        elif self.score >= 50:
            return 'orange'
        else:
            return 'red'

    @property
    def has_html(self):
        """✅ Ar turi HTML reportą"""
        return bool(self.report_html)

    @property
    def vehicle_info(self):
        """✅ Gauti transporto priemonės info"""
        if self.report_data:
            return self.report_data.get('yearMakeModel', f'VIN: {self.vin}')
        return f'VIN: {self.vin}'


class Transaction(models.Model):
    """
    Mokėjimų istorijos modelis
    Saugo visus pinigų įkėlimus ir nuėmimus
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHODS = (
        ('stripe', 'Stripe'),
        ('blik', 'BLIK'),
        ('przelewy24', 'Przelewy24'),
        ('card', 'Credit Card'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PLN')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True)

    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} - {self.status}"

    def mark_completed(self):
        """Pažymėti transakciją kaip užbaigtą"""
        self.status = 'completed'
        self.save()
        self.user.profile.add_balance(self.amount)

    def mark_failed(self):
        """Pažymėti transakciją kaip nepavykusią"""
        self.status = 'failed'
        self.save()


class ReportPackage(models.Model):
    """
    Ataskaitų paketų modelis
    Saugo nupirktus ataskaitų paketus (1, 10, 100)
    """
    PACKAGE_TYPES = (
        ('1', '1 Report'),
        ('10', '10 Reports'),
        ('100', '100 Reports'),
    )

    REPORT_TYPES = (
        ('carfax', 'Carfax'),
        ('autocheck', 'Autocheck'),
        ('nmvtis', 'NMVTIS'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages')
    package_type = models.CharField(max_length=3, choices=PACKAGE_TYPES)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    reports_remaining = models.IntegerField()
    total_reports = models.IntegerField()

    purchased_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'report_packages'
        verbose_name = 'Report Package'
        verbose_name_plural = 'Report Packages'
        ordering = ['-purchased_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_package_type_display()} {self.get_report_type_display()}"

    def use_report(self):
        """Panaudoti vieną ataskaitą iš paketo"""
        if self.reports_remaining > 0:
            self.reports_remaining -= 1
            if self.reports_remaining == 0:
                self.is_active = False
            self.save()
            return True
        return False


class APILog(models.Model):
    """
    API užklausų logging modelis
    Saugo visas užklausas į Carfax, Autocheck, NMVTIS API
    """
    API_PROVIDERS = (
        ('carfax', 'Carfax'),
        ('autocheck', 'Autocheck'),
        ('nmvtis', 'NMVTIS'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.CharField(max_length=20, choices=API_PROVIDERS)
    vin = models.CharField(max_length=17)
    request_data = models.JSONField(default=dict, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    status_code = models.IntegerField()
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_logs'
        verbose_name = 'API Log'
        verbose_name_plural = 'API Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.provider} - {self.vin} - {'Success' if self.success else 'Failed'}"
