from django import forms
from .models import Recipe, RecipeIngredients
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from food.models import Food
from .fields import ListTextWidget


class RecipeModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'recipe-create__form__input'})
        self.fields['images'].widget.attrs.update({'class': 'recipe-create__form__input recipe-create__form__input--images'})
        self.fields['published'].widget.attrs.update({'class': 'recipe-create__form__input recipe-create__form__input--publish'})
    
    class Meta:
        model = Recipe
        fields = ('title', 'portions', 'content', 'images',
                  'prepare_time', 'tags', 'published')
        widgets = {
            'prepare_time': forms.TimeInput(format='%H:%M', 
            attrs={'type': 'time'}
            ),
        }


IngredientFormSet = (inlineformset_factory(Recipe, RecipeIngredients, fields=[
    'ingredient', 'quantity', 'unit'], widgets={'ingredient':ListTextWidget(), 'class':'recipe-create__ingredients__input'}, extra=0, min_num=1, validate_min=True, can_delete=True))
