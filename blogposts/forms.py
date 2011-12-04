from django import forms
from blogposts.models import Blogpost

class BlogpostForm(forms.ModelForm):
    class Meta:
        model = Blogpost
        exclude = ('author','slug', 'pub_date')
        
