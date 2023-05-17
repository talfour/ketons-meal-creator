from django import forms
from .models import Answer, Question, Category


class QuestionModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'new-question__form__form__input'})

    class Meta:
        model = Question
        fields = ('title', 'content','category')


# class CategoryModelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CategoryModelForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class':'new-category-form__form__input'})

#     class Meta:
#         model = Category
#         fields = ('name',)

class AnswerModelForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(AnswerModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'question__answer-form__form__input'})

    text = forms.CharField(label="",widget=forms.Textarea(attrs={'placeholder':'Tutaj wpisz odpowiedź', 'rows':'10', 'cols':'40'}))
    class Meta:
        model = Answer
        fields = ('text',)
        