from django import forms
from accounts.models import CustomUser

# create forms 
class UpdateLocationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['location', ]