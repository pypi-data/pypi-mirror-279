from django import forms
from artd_shopify.models import (
    ShopifyAppCredential,
    ShopifyApiCredential,
    ShopifyGraphQlCredential,
)


class ShopifyAppCredentialForm(forms.ModelForm):
    class Meta:
        model = ShopifyAppCredential
        fields = [
            "api_password",
        ]
        widgets = {
            "api_password": forms.PasswordInput(),
        }


class ShopifyApiCredentialForm(forms.ModelForm):
    class Meta:
        model = ShopifyApiCredential
        fields = [
            "access_token",
        ]
        widgets = {
            "access_token": forms.PasswordInput(),
        }


class ShopifyGraphQlCredentialForm(forms.ModelForm):
    class Meta:
        model = ShopifyGraphQlCredential
        fields = [
            "access_token",
            "api_secret",
        ]
        widgets = {
            "api_secret": forms.PasswordInput(),
            "access_token": forms.PasswordInput(),
        }
