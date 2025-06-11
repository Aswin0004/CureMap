from django import forms
from .models import FamilyMember

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'relationship', 'custom_relationship', 'photo']
