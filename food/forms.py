from django import forms
from .models import Food


class FoodModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FoodModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'food-new__form__field__input'})
            if field.widget.input_type == "number":
                field.widget.attrs['min'] = 0

    class Meta:
        model = Food
        exclude = ['created', 'slug', 'user']

    def clean(self):
        skip = ['name', 'category']

        for field_name in self.fields.items():            
            if field_name[0] not in skip:
                if self.cleaned_data[f'{field_name[0]}'] < 0:
                    self.add_error(f'{field_name[0]}', 'Wartość nie może być ujemna')
        
            
                