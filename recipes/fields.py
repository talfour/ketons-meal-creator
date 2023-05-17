from django import forms
from food.models import Food

class ListTextWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self.attrs.update({'list':'list__ingredients'})
        self.attrs.update({'class':'recipe-create__ingredients__choosen hidden'})

    def render(self, name, value, attrs=None, renderer=None):
        food = Food.objects.filter(user_id=1)
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = f'<datalist id="list__ingredients">'
        for item in food:
            data_list += f'<option value="{item}" data-value={item.id}>' 
        data_list += '</datalist>'

        return (text_html + data_list)