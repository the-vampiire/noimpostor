from django.forms import ModelForm
from .models import Accomplishment

class AccomplishmentForm(ModelForm):
    class Meta:
        model = Accomplishment
        exclude = ('user',)
