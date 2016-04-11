from django import forms
from models import *

class studentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = student
        fields = ('name', 'email', 'password', 'id1', 'reg_done', 'semester', 'branch', 'mess_dues', 'lib_dues', 'reg_fees', 'mess_fees')