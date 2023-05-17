from django import forms
from .models import Profile
from recipes.models import RecipeEvent, Recipe
from django.db.models import Q


class ProfileModelForm(forms.ModelForm):

    """Form used to populate user information."""

    def __init__(self, *args, **kwargs):
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].label = "Zmień awatar"
        for field in self.fields.values():
            field.widget.attrs.update({'class':'profile-update-form__form__input'})
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar',
                  'gender', 'weight', 'height', 'age', 'activity', 'diet_type', 'target', 'is_on_adaptation', 'want_to_type_nutritiens', 'total_kcal', 'proteins', 'carbs', 'fats')
        labels = {
            'want_to_type_nutritiens': 'Chce samodzielnie ustawić wartości',
            'is_on_adaptation': 'Czy jesteś na adaptacji?',
            'avatar': 'Zmień awatar',

        }
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': '.jpg, .jpeg, .png'}),
            
        }


class AddNewMealForm(forms.ModelForm):
    class Meta:
        model = RecipeEvent
        exclude = ('user', 'date')
        

    def __init__(self, user, *args, **kwargs):
        super(AddNewMealForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'calendar-new-meal__form__input'})
        choices = []
        self.fields['recipe'].label = "Przepis"
        self.fields['portions'].label = "Ilość porcji"
        self.fields['description'].label = "Nazwa posiłku"
        self.fields['time'].label = "Czas spożycia"
        for obj in Recipe.objects.filter(Q(author=user) | Q(saved=user)).all().order_by('title'):
            choices.append((obj.id, obj.title))
        self.fields['recipe'].choices = choices
        
    def clean(self):
        data = self.cleaned_data
        recipe = data['recipe']
        recipe_portions = recipe.portions
        portions = data['portions']
        if portions > recipe_portions:
            raise forms.ValidationError(f"Max portions you can choose is {recipe_portions}")
        