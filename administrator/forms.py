from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Calls, Incidence, Response

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_names', 'user_type', 'location', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_names', 'user_type', 'location']


# Forms 
class RecordCallForm(forms.ModelForm):
    class Meta:
        model = Calls
        fields = ('caller_name', 'caller_phone', 'location', 'priority', )


class IncidenceForm(forms.ModelForm):
    class Meta:
        model = Incidence
        fields = ('incidence_type', 'call', 'location', 'desc', 'status', )


class AssignResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('message', )