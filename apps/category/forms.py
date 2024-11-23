from django import forms

from blog.models import Category, Topic


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'meta_title', 'meta_description', 'meta_keywords']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'category', 'description', 'meta_title', 'meta_description', 'meta_keywords']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }