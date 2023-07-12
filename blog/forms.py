from django import forms
from tinymce.widgets import TinyMCE
from .models import Post

def min_length_3(value):
    if len(value) < 3:
        raise forms.ValidationError("Kendi denetimim")


class PostModelForm(forms.ModelForm):
    tag = forms.CharField()
    content = forms.CharField(widget=TinyMCE(attrs={'cols':40, 'rows':20}))
    # title = forms.CharField(validators=[validators.MinLengthValidator(3)])
    title = forms.CharField(validators=[min_length_3])
    class Meta:
        model = Post
        fields = [
            'title', 
            'cover_image',
            'content',
            'category',
            'tag',
        ]


    # def clean(self):
    #     title = self.cleaned_data.get('title')
    #     if len(title) < 3:
    #         raise forms.ValidationError('En Az Üç Karakter')
    #     return title
