from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='First Name', 
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    last_name = forms.CharField(required=True, label='Last Name', 
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(required=True, label='Username', 
                               help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    email = forms.EmailField(required=True, label='Email', 
                             help_text='Required. Enter a valid email address.', 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password1 = forms.CharField(required=True, label='Password', 
                                 help_text='Required. Enter a valid password.', 
                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    password2 = forms.CharField(required=True, label='Password confirmation', 
                                 help_text='Enter the same password as before, for verification.', 
                                 widget=forms.PasswordInput(attrs={'class': 'form-control'})) 

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class TradeCalculator(forms.Form):

    trade_selection = (
            ("short", "Short Trade"),
            ("long", "Long Trade"),
            )

    trade_options = forms.ChoiceField(choices=trade_selection, required=True)

    entry_price = forms.FloatField(
        label="Entry Price",
        required=True,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"placeholder": "Enter a Entry Price", "step": 0.00000001}
        ),
    )

    entry_line_a = forms.FloatField(
        label="Line One Entry Price",
        required=True,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"placeholder": "1st Entry Price above(short) or below(long)", "step": 0.00000001}
        ),
    )

    entry_line_b = forms.FloatField(
        label="Line Two Entry Entry Price",
        required=True,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"placeholder": "2nd Enter Price above(short) or below(long)", "step": 0.00000001}
        ),
    )

    leverage_entry = forms.FloatField(
        label="Leverage",
        required=True,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Enter a Leverage (1 - 1000)",
                "step": 1.0,
            }
        ),
    )

    # target = forms.FloatField(
    #     label="Targeted Value",
    #     required=True,
    #     min_value=0,
    #     widget=forms.NumberInput(
    #         attrs={"placeholder": "Enter a Targeted Value", "step": 1.0}
    #     ),
    # )

    account_size = forms.FloatField(
            label="Account Size",
            required=True,
            min_value=0,
            widget=forms.NumberInput(
                attrs={"placeholder": "Enter Your Account Size",
                       "step": 1.0}
                ),
            )

    def clean(self):
        cleaned_data = super().clean()
        trade_options = cleaned_data.get("trade_options")
        entry_price = cleaned_data.get("entry_price")
        entry_line_a = cleaned_data.get("entry_line_a")
        entry_line_b = cleaned_data.get("entry_line_b")

        if trade_options == "short":
            if entry_price is not None and entry_line_a is not None and entry_line_b is not None:
                if entry_price > entry_line_a:
                    raise ValidationError("Short Trade: Entry Price at Line 1 is less than the Entry Price")

                if entry_line_a > entry_line_b:
                    raise ValidationError("Short Trade: Entry Price at Line 1 is greater than the Entry Price at Line 2")
        elif trade_options == "long":
            if entry_price is not None and entry_line_a is not None and entry_line_b is not None:
                if entry_price < entry_line_a:
                    raise ValidationError("Long Trade: Entry Price is greater than the Entry Price at Line 1")
                if entry_line_a < entry_line_b:
                    raise ValidationError("Long Trade: Entry Price at Line 2 is greater than the Entry Price at Line 1")

        return cleaned_data


class ChangeExpirationTimeForm(forms.Form):
    time_value = forms.IntegerField(label='Time Value', help_text='Enter a value for time (e.g., 10 for 10 minutes or 5 for 5 days).')
    time_unit = forms.ChoiceField(label='Time Unit', choices=[
        ('days', 'Days'),
        ('hours', 'Hours'),
        ('minutes', 'Minutes'),
    ])

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    package = forms.ChoiceField(choices=[
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ])
    message = forms.CharField(widget=forms.Textarea)
