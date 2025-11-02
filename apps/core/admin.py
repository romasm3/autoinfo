"""
DJANGO ADMIN PANEL
Registruoja modelius admin panelėje su custom displays
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Report, Transaction, ReportPackage, APILog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    UserProfile admin konfigūracija
    Rodo: user, balance (su spalva), phone, created_at
    """
    list_display = ('user', 'balance_display', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone')
        }),
        ('Financial', {
            'fields': ('balance',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def balance_display(self, obj):
        """Rodyti balansą su spalva"""
        color = '#28a745' if obj.balance > 0 else '#dc3545'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} PLN</span>',
            color,
            obj.balance
        )
    balance_display.short_description = 'Balance'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Report admin konfigūracija
    Rodo: VIN, user, report type, score (su spalva), accidents, owners
    """
    list_display = ('vin', 'user', 'report_type', 'score_display', 'accidents', 'owners', 'price_paid', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('vin', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'vin', 'report_type')
        }),
        ('Report Data', {
            'fields': ('score', 'accidents', 'owners', 'report_data')
        }),
        ('Financial', {
            'fields': ('price_paid',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def score_display(self, obj):
        """Rodyti score su spalva pagal reikšmę"""
        if obj.score is None:
            return '-'

        # Spalvos: žalia (70+), geltona (50-69), raudona (<50)
        if obj.score >= 70:
            color = '#28a745'
        elif obj.score >= 50:
            color = '#ffc107'
        else:
            color = '#dc3545'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/100</span>',
            color,
            obj.score
        )
    score_display.short_description = 'Score'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Transaction admin konfigūracija
    Rodo: transaction ID, user, amount, payment method, status (su badge)
    """
    list_display = ('transaction_id', 'user', 'amount_display', 'payment_method', 'status_display', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'transaction_id')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'transaction_id', 'amount', 'currency')
        }),
        ('Payment', {
            'fields': ('payment_method', 'status', 'description')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def amount_display(self, obj):
        """Rodyti sumą su valiuta"""
        return format_html('{} {}', obj.amount, obj.currency)
    amount_display.short_description = 'Amount'

    def status_display(self, obj):
        """Rodyti status su spalvotu badge"""
        colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'failed': '#dc3545',
            'refunded': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'


@admin.register(ReportPackage)
class ReportPackageAdmin(admin.ModelAdmin):
    """
    ReportPackage admin konfigūracija
    """
    list_display = ('user', 'package_type', 'report_type', 'reports_remaining', 'total_reports', 'is_active', 'purchased_at')
    list_filter = ('package_type', 'report_type', 'is_active', 'purchased_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('purchased_at',)
    date_hierarchy = 'purchased_at'


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    """
    APILog admin konfigūracija
    """
    list_display = ('provider', 'vin', 'user', 'success_display', 'status_code', 'created_at')
    list_filter = ('provider', 'success', 'created_at')
    search_fields = ('vin', 'user__username', 'error_message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def success_display(self, obj):
        """Rodyti success su checkmark/cross"""
        if obj.success:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Success</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ Failed</span>')
    success_display.short_description = 'Status'


# Admin site customization
admin.site.site_header = "AutoInfo Administration"
admin.site.site_title = "AutoInfo Admin"
admin.site.index_title = "Dashboard"
