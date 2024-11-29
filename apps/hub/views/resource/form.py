from django import forms

from hub.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['project', 'name', 'url', 'description']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
