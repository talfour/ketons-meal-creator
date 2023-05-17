from django import template

register = template.Library()

@register.simple_tag
def dictKeyLookup(the_dict, key):
    if the_dict.get(key, '') == '':
        return 0
    else:
        return round(the_dict.get(key, ''),1)

@register.filter
def total_kcal(obj):
    kcal = 0
    for i in obj:
        for j in i.recipe.recipeingredients_set.all():
            kcal += j.get_nutrition_info['calories']
    return kcal

@register.filter
def total_proteins(obj):
    proteins = 0
    for i in obj:
        for j in i.recipe.recipeingredients_set.all():
            proteins += j.get_nutrition_info['proteins']
    return proteins

@register.filter
def total_carbs(obj):
    carbs = 0
    for i in obj:
        for j in i.recipe.recipeingredients_set.all():
            carbs += j.get_nutrition_info['carbs']
    return carbs

@register.filter
def total_fats(obj):
    fats = 0
    for i in obj:
        for j in i.recipe.recipeingredients_set.all():
            fats += j.get_nutrition_info['fats']
    return fats

@register.filter
def total_saturated_fats(obj):
    saturated_fats = 0
    for i in obj:
        for j in i.recipe.recipeingredients_set.all():
            saturated_fats += j.get_nutrition_info['saturated_fats']
    return saturated_fats

@register.filter
def total_fibre(obj):
    fibre = 0
    for i in obj:
        for j in i.recipe.recipeingredients_set.all():
            fibre += j.get_nutrition_info['fibre']
    return fibre

@register.filter
def divide_portions(obj):
    for i in obj:
        i.recipe.portions

