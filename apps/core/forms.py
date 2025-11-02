"""
╔══════════════════════════════════════════════════════════╗
║  DJANGO FORMS                                            ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/forms.py                 ║
║  PASKIRTIS: Formos su validacija                        ║
╚══════════════════════════════════════════════════════════╝
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.ModelForm):
    """
    Supaprastinta registracijos forma - TIK EMAIL IR PASSWORD
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'john@example.com'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        }),
        label='Password'
    )
    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        }),
        label='Confirm Password'
    )
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        """Validuoti ar email jau neegzistuoja"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email.lower()

    def clean(self):
        """Validuoti ar slaptažodžiai sutampa"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        """Išsaugoti user su email kaip username"""
        user = super().save(commit=False)
        # Naudoti email kaip username
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Prisijungimo forma - EMAIL IR PASSWORD
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'john@example.com',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class VINSearchForm(forms.Form):
    """VIN paieškos forma"""
    REPORT_CHOICES = (
        ('carfax', 'Carfax'),
        ('autocheck', 'Autocheck'),
        ('nmvtis', 'NMVTIS'),
    )

    vin = forms.CharField(
        max_length=17,
        min_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 17-character VIN',
            'maxlength': '17',
            'style': 'text-transform: uppercase;'
        })
    )
    report_type = forms.ChoiceField(
        choices=REPORT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_vin(self):
        """VIN validacija"""
        import re
        vin = self.cleaned_data.get('vin', '').upper()

        if len(vin) != 17:
            raise forms.ValidationError('VIN must be exactly 17 characters.')

        if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
            raise forms.ValidationError('Invalid VIN format.')

        return vin


class AddFundsForm(forms.Form):
    """Pinigų įkėlimo forma"""
    AMOUNT_CHOICES = (
        ('10', '10 PLN'),
        ('25', '25 PLN'),
        ('50', '50 PLN'),
        ('100', '100 PLN'),
        ('250', '250 PLN'),
        ('500', '500 PLN'),
        ('custom', 'Custom Amount'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('stripe', 'Credit Card (Stripe)'),
        ('blik', 'BLIK'),
        ('przelewy24', 'Przelewy24'),
    )

    amount_choice = forms.ChoiceField(
        choices=AMOUNT_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    custom_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom amount (min 10 PLN)',
            'step': '0.01'
        })
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        amount_choice = cleaned_data.get('amount_choice')
        custom_amount = cleaned_data.get('custom_amount')

        if amount_choice == 'custom':
            if not custom_amount:
                raise forms.ValidationError('Please enter a custom amount.')
            if custom_amount < 10:
                raise forms.ValidationError('Minimum amount is 10 PLN.')

        return cleaned_data

    def get_amount(self):
        """Grąžina galutinę sumą"""
        amount_choice = self.cleaned_data.get('amount_choice')
        if amount_choice == 'custom':
            return self.cleaned_data.get('custom_amount')
        return float(amount_choice)


class ContactForm(forms.Form):
    """Kontaktų forma"""
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message...',
            'rows': 5
        })
    )
