from django import forms

from category.models import Topic
from blog.models import BlogPost, Volume


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title', 'content', 'thumbnail', 'status', 
            'category', 'topics', 'post_type', 'volume', 'is_featured', 
            'is_spotlighted'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'topics': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'volume': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        category_id = kwargs.pop('category_id', None)
        super().__init__(*args, **kwargs)
        if category_id:
            self.fields['topics'].queryset = Topic.objects.filter(category_id=category_id)
        else:
            self.fields['topics'].queryset = Topic.objects.none()

        if not self.user.is_admin:
            self.fields.pop('is_featured')
            self.fields.pop('is_spotlighted')

        self.fields['volume'].queryset = Volume.objects.all()
        self.fields['volume'].required = False
