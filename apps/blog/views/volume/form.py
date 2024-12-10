from django import forms

from blog.models import Volume



class VolumeForm(forms.ModelForm):
    class Meta:
        model = Volume
        fields = ['number', 'title', 'description']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
