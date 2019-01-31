from django import forms

from captcha import fields


class TestWizardRecaptchaForm(forms.Form):
    charfield = forms.CharField()
    captcha = fields.ReCaptchaField(wizard_persist_is_valid=True)
