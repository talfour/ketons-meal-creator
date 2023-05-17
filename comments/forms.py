from django import forms
from .models import Comment
from django.forms.widgets import TextInput, Textarea

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'comment__reply-form__text-area', 'placeholder':'Twój komentarz'}))

    """Form used to add comments."""
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""
        
    class Meta:
        model = Comment
        exclude = ('timestamp', 'content_object','user', 'parent')
        labels = {
            'content': ''
        }
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id':forms.HiddenInput()
        }

    # content_type = forms.CharField(widget=forms.HiddenInput)
    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    # # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # content = forms.CharField(widget=forms.Textarea)