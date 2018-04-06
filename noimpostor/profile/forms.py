from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import DefaultPrivacy

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

class DefaultPrivacyForm(ModelForm):
    class Meta:
        model = DefaultPrivacy
        fields = ['setting']
